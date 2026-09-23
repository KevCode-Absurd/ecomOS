# Store Setup — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Platform/theme
- catalog
- markets
- payments
- shipping
- policies
- access boundaries

## Measures
- Successful test purchase
- launch blockers
- checkout errors

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Know which three Shopify admin areas actually run the store** (`d082e7bbfa8ab1aab86e6b89`): Reduce admin overwhelm to Products, Online Store and Settings, the three sections that control selling, appearance and configuration.
  Applies when: Orienting yourself in a new Shopify admin before adding products, designing the storefront or configuring checkout.
  Condition: Admin layout and menu labels change between Shopify releases; verify the current interface rather than hunting for exact labels.

- **Verifying each setup step actually worked** (`d6854b97be2c5cbde333cc32`): Close out each store configuration step with a concrete check, because a saved setting is not proof that checkout, tax or links behave correctly.
  Applies when: You have configured a store section such as payments, shipping or domains and want to confirm it works before relying on it.
  Condition: Some checks, such as DNS propagation, are outside your control and only show status rather than instant confirmation.
  Condition: Test mode verifies logic but does not prove a live payment settles; complete any live transaction test the current Shopify process requires.

- **Doing store setup in the right order to avoid launch breakage** (`a14524485a100465118a5c47`): Sequence Shopify setup so identity, payments, tax, shipping, domain and tracking are configured before testing and removing the password gate.
  Applies when: You are planning the launch sequence and want to avoid discovering broken checkout or tax settings after customers arrive.
  Condition: This is the source's emphasis on order of operations, not a claim that any other sequence is impossible; it identifies what tends to break if steps are out of order.
  Condition: The source warns that interfaces change, so the exact screens for each step should be confirmed in the current Shopify admin.

## Prepare a store for launch
Workflow ID: `store-setup.launch-store`

**Deliverable:** Launch checklist with evidence and blockers

### Proposed decision sequence
1. Check product availability, prices and fulfilment settings
2. Walk a representative purchase journey in the appropriate test environment
3. Assign launch blockers and verify their resolution before release

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Make a product actually buyable before launch
Card: `d7c81282140d8c0a9cd5de68` · Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx · Section: 1

The minimum product-admin steps to stop a new product from showing sold out or unaddable-to-cart at launch.

Applies when: Immediately before driving paid traffic or launch content to a new product, to avoid wasting spend on an unbuyable PDP.

- Go to Products, Edit product on the SKU you are launching.
- Set Available inventory (the source example used a large number like 10,000 for a launch SKU) and Save.
- If drop shipping, confirm the fulfillment app or supplier actually holds that stock — Shopify inventory is only a number and does not create real stock.
- After saving, add the product to cart yourself on the live store to confirm it is purchasable and the variant/price is correct.
- **Condition:** Setting a large inventory number on a drop-ship SKU does not guarantee fulfillment; keep it aligned with real supplier stock.
- **Condition:** If you later toggle inventory tracking, re-check the PDP still allows purchase.

#### Doing store setup in the right order to avoid launch breakage
Card: `a14524485a100465118a5c47` · Source: The OFFICIAL Shopify 2026 Tutorial.docx · Section: 0

Sequence Shopify setup so identity, payments, tax, shipping, domain and tracking are configured before testing and removing the password gate.

Applies when: You are planning the launch sequence and want to avoid discovering broken checkout or tax settings after customers arrive.

- Configure account identity and store settings first, since country, currency and store name affect the defaults of downstream tax and payment screens.
- Set up payments with exact legal identity next, then taxes and physical presence, then shipping zones and package weights, because shipping rates depend on weight data and tax regions depend on where you have presence.
- Connect the custom domain and business email after the store operational settings, so the store is reachable at the final address when you begin testing.
- Install tracking and create the legal pages, then run test-mode orders as the gate that verifies checkout, taxes, shipping rates and policy links together.
- Remove the store password only after the test order passes; the source treats un-gating as the last step, not an early one.
- **Condition:** This is the source's emphasis on order of operations, not a claim that any other sequence is impossible; it identifies what tends to break if steps are out of order.
- **Condition:** The source warns that interfaces change, so the exact screens for each step should be confirmed in the current Shopify admin.

#### Pre-Launch Store Configuration Checklist (Topic Map)
Card: `9237bdf8aa5bda61e30903eb` · Source: WooCommerce Tutorial for Beginners 2026.docx · Section: 0

A four-part coverage map for a WooCommerce build — domain/email, store configuration, payments/tax, and shipping profiles — to verify nothing was skipped before launch.

Applies when: You are auditing a WooCommerce store before going live and want to confirm each configuration area is actually done rather than assumed.

- Domain and email: confirm the store's domain resolves and transactional email (order confirmations, password resets) actually sends and lands in inboxes — not just spam.
- Store configuration: WordPress installed, theme (e.g. Blocksy) active, page builder (e.g. Elementor) working, store address and currency set correctly.
- Products: at least one Simple Product and one Variable Product published, with prices, stock thresholds, weights/dimensions, and categories assigned.
- Payments and tax: Stripe and PayPal connected and connection-tested, tax plugin configured against the correct store address and calculation basis, test order completed.
- Shipping profiles: zones created for each region, flat vs free-shipping thresholds set deliberately, Shipping Classes assigned to heavy/oversized items and costed.
- Mobile: check key pages on a phone viewport and fix with Elementor responsive toggles.
- Finish with a full test purchase in Test mode before flipping payments to Live.
- **Condition:** This is a coverage map for baseline configuration — page copy, analytic accuracy, and ongoing speed work belong to separate disciplines and are not covered here.
- **Condition:** Do not treat 'plugin installed' as 'plugin configured'; the test order is the real verification.

### Retrieval and applicability
Search: `store setup launch buyable inventory payments shipping`
Related domains: measurement, speed, bot-and-agent-security
Mixed-folder candidate IDs: c780e415d44d2c082be2c7bd, 4e93962abaeb495f4bfa02fa, 7e066cd286cd76bed76d6b20

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

## Specify a storefront template change
Workflow ID: `store-setup.change-template`

**Deliverable:** Implementation brief and acceptance checks

### Proposed decision sequence
1. Document current behaviour and required shopper outcome
2. Specify a scoped change with backup and rollback instructions
3. Verify mobile, product selection and purchase-path behaviour

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Publish a Custom PDP into Shopify as a Reusable Section
Card: `c7884fec6d58eb177a45a865` · Source: Claude & Shopify Built $750k_m Ai Powered Ecom Brand.docx · Section: 2

Ship a designed product page into Shopify by pasting the generated code as a Liquid section file, then adding it to a product template.

Applies when: Moving a page built in an external page designer into a live Shopify store.

- In Shopify admin go to Online Store, then edit the theme code, and create a new section file with a clear naming convention (source used a WLE/brand/product prefix plus the .liquid extension).
- Paste the generated page code into that section file and save; the file is then stored permanently in the store and can be deleted later if needed.
- Create the product in Products, upload images, set the selling price (source used the supplier's recommended price of 21.50), and confirm inventory is not zero — the source set available units to 10,000 so the page would not show 'sold out'.
- Under the theme's product templates, create a new template for this product and hide the default theme sections you do not want.
- Add a section and select your custom section from the list; the whole page loads in.
- In the section settings, explicitly select the product — the source says this is 'the biggest thing' to do — which then populates images and price automatically.
- Reorder, show or hide individual blocks within the section to match your preferred merchandising.
- Verify the current Shopify theme editor steps in your admin, as menus and labels change.
- **Condition:** Custom Liquid sections need maintenance when the theme updates.
- **Condition:** Bundles and subscription options are configured separately in the product area, not inside the page section.

#### Build richer static pages with templates instead of plain text
Card: `fe0d110afd3a8e574595786f` · Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx · Section: 4

Turn flat pages like About Us into designed pages by creating templates and assigning them.

Applies when: Creating or upgrading About Us, story or other static content pages.

- A page with only text pasted into the admin renders as a plain static page.
- To design it, create a template for that page and build it with sections like any other page on the store: image-with-text-overlay for a brand image, rich text for the story, image-with-text blocks, scrolling panels, video-with-text.
- Fill content directly in the template sections; because static pages don't vary per product, meta fields are unnecessary here.
- Remove sections you don't need and flip image/text orientation for variety.
- Save the template, then go back to the page in the admin and assign the template from the template selector.
- Apply the same template logic to any other page you want to look designed rather than static.
- **Condition:** Templates must be assigned to the page after creation or the design won't appear.

#### Turn a default theme into a brand with global settings and a transparent logo
Card: `ba017a5df3452f73a52cf85e` · Source: Shopify Store Setup Full Tutorial 2026_ Step by Step.docx · Section: 0

The fast foundational pass — hero H1, colors, typography, logo — that makes a template feel intentional before deeper section work.

Applies when: Customizing a freshly published theme so it stops looking generic and starts reading as a real brand.

- Open Edit theme. The left panel lists sections; the right panel is a live preview you refresh as you change things.
- Start with the header structure and alignment even if your logo is not ready yet.
- Go to Theme settings > Colors: set the primary brand color and keep the background white. The source argues white backgrounds generally convert better because products stand out on them.
- Go to typography settings and choose simple, readable fonts (the source names Montserrat and Source Sans Pro). Decorative fonts are explicitly called a clarity risk — if customers struggle to read, they leave.
- Generate a minimal logo with an AI image tool or free logo tools; text-based logos work well. Then use a background remover such as remove.bg to export a transparent PNG — the source calls messy logo backgrounds a common beginner mistake that instantly lowers perceived quality.
- Upload via the header/theme settings and adjust size so it looks balanced, not oversized or tiny.
- Optionally build a cohesive palette by asking an AI for a primary, secondary and accent hex set, then paste the primary hex into the color field and keep contrast high so text stays legible.
- Optionally use the theme editor's AI section recommendations: describe your brand in a few sentences and it generates layout suggestions for your niche.
- **Condition:** AI-generated palettes and sections are starting points; you still apply and review them inside the theme editor.
- **Condition:** White background and font choices are the source's conversion-oriented opinions, not tested rules for every brand.

### Retrieval and applicability
Search: `Shopify template Liquid section theme product`
Related domains: measurement, speed, bot-and-agent-security
Mixed-folder candidate IDs: 93d8ebb61724a2769e27830f, c3cde0fb26434b87df3b1727, 577a55dfd0ec83ba51d8e550

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

## Audit store readiness
Workflow ID: `store-setup.audit-store`

**Deliverable:** Store readiness audit

### Proposed decision sequence
1. Inspect catalog, navigation and essential product information
2. Check market-specific payment, delivery and policy clarity
3. Prioritise broken purchase paths over cosmetic improvements

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Run a Pre-Launch Audit of Products, Policies and Navigation
Card: `ab549d0194fc9ddaddcdb0f1` · Source: The OFFICIAL Shopify 2026 Tutorial.docx · Section: 1

Use Sidekick to scan for missing descriptions, prices and images, generate required policy pages, then do a final click-through of the store as a first-time visitor.

Applies when: Final quality pass before removing password protection, when the builder has been staring at the store too long to spot obvious errors.

- Ask Sidekick to scan the product list for missing descriptions or prices; Sidekick is described as effective at catching missing product images, pricing gaps and half-finished details.
- Ask Sidekick to verify all contact, shipping and return policies are set up correctly.
- Ensure the essential pages exist before launch: contact page, shipping policy, return policy, privacy policy and terms of service — these affect both customer trust and how Google evaluates the site.
- Generate first drafts of policies by asking Sidekick (e.g. a shipping policy, or a return policy for a clothing business with a 30-day window), then customize to match actual practices.
- Do a final walkthrough as a first-time visitor: click through navigation, add an item to the cart, and complete checkout in test mode.
- Confirm shipping rates look right and all payment options work with test card numbers rather than a real card.
- Repeat the walkthrough on a phone before launch.
- **Condition:** AI-generated policies are starting points to customize, not legal documents to publish unedited.
- **Condition:** The source frames missing policy pages as a red flag for both shoppers and search engines; it does not promise a ranking outcome.

#### Configure cart behavior: drawer vs page and free shipping bar
Card: `ed834e77dbd7bccfdbb5194b` · Source: Shopify for Beginners_ Everything From Setup to Your First Sale.docx · Section: 2

Choose whether Add to cart opens a cart drawer or navigates to the cart page, and whether to add a free shipping bar, since it affects how easily shoppers keep browsing.

Applies when: Setting up cart experience before launch, and optimizing how customers proceed from product to checkout.

- In theme settings' Cart options, choose between 'drawer' and 'page'. Drawer opens a popup overlay; page sends the shopper to the cart page.
- Prefer the drawer: the presenter argues page cart forces shoppers to click back to keep browsing, making it worse for browsing flow. Confirm this against your own store's data rather than treating it as universal.
- Optionally add a free shipping bar in the cart drawer and customize its colors, so shoppers see progress toward free shipping.
- Test the actual add-to-cart flow via quick buy and normal product page to confirm the drawer/page setting applies consistently in your theme.
- Review cart-related theme settings for anything else (e.g. cart notes, upsell blocks) that the theme exposes, and skip settings you won't use.
- **Condition:** Drawer vs page preference is a stated opinion; some stores/traffic convert better on the cart page. Test rather than assume.
- **Condition:** Available cart settings vary by theme.

#### Build Store Front-End Structure That Mirrors Top Ecommerce Sites
Card: `c39aeb8d4ca961859a00d1db` · Source: WooCommerce Tutorial 2026_ Complete MasterClass for Beginners.docx · Section: 1

Lay out the storefront with the standard components shoppers expect on the homepage, shop and product pages.

Applies when: Planning homepage and shop-page sections for a new store, so shoppers can search, browse and buy without friction.

- Header: logo left, navigation menu centre, and search, account and cart buttons right. Make the cart a mini-cart drawer that opens from the side and links to the full cart page.
- My Account should let customers manage orders, delivery addresses and account details so they self-serve instead of contacting you.
- Homepage order used in the build: banner, call-to-action, best-selling products with add-to-cart, a category section, latest products with a countdown offer, testimonials for trust, blog posts, and a footer.
- Shop page: product grid with add-to-cart and wishlist heart buttons, plus sidebar widgets — product search, price filter, recently viewed products, and category/tag filters.
- Product page: name, description, images, variations, a stock progress bar showing remaining stock, quantity selector, add-to-cart, full description, additional information, reviews and related products.
- Cart and checkout: allow removing items and editing quantities in the cart, then checkout with contact details, billing address, payment method choice, a coupon field that discounts automatically, an order summary showing tax, discount, subtotal and total, and a thank-you page after the order is placed.
- **Condition:** This is a conventional structure the source copied from large marketplaces, not a validated conversion benchmark — treat each section as a hypothesis to test for your catalog.
- **Condition:** A stock progress bar can create urgency or backfire by discouraging purchase when stock looks low; test it.

### Retrieval and applicability
Search: `store setup navigation checkout product trust`
Related domains: measurement, speed, bot-and-agent-security
Mixed-folder candidate IDs: e0ab1f148d59388bd486efa0, e6fb10561aef213b43d079cb, e1020c15977b0bf8dd0999d4

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
