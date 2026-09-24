# How to Create an Ecommerce Website with WordPress 2026 (step by step)

source_id: 1Wkwgmn2r1WmdIXB9ionMa7wpQXdSAucF | folder: /05-SET-store-setup | cards: 25 | words: 11,495 | type: video transcript (tutorial)

credibility: Presenter is Dale, a website-building content creator ("Creator Pro website"). He is a Hostinger affiliate and states this directly (a special discount link, a "Creator Pro website" coupon code). No stated agency, client or store results; evidence is a single demo build (an electronics store, "Kova Echo" headphones) he narrates live. This is walkthrough demonstration, not a case study with outcomes.

date signals: Video references a "Black Friday" sale and the date "November 17th" (no year stated in transcript) and is filed under "2026" in its own title. Hostinger pricing given ($3.38/month on the sale shown, ~$4/month off-sale) is explicitly time-bound by the presenter himself. Uses Astra theme, Starter Templates plugin, Elementor page builder, and WooCommerce — all named versions current as of the recording; the source itself warns these interfaces change and to distrust tutorials older than ~18 months. [web check: current Astra/Elementor/WooCommerce UI and Hostinger pricing]

## 1. What this source is for

Takes an operator from zero to a live WooCommerce store on WordPress: buying hosting and a domain, installing WordPress, installing a theme and page builder, importing a starter template, building and styling pages in Elementor, adding products (simple and variable), connecting Stripe and PayPal, configuring shipping zones and a welcome coupon, making the site mobile-responsive, and flipping the store from "coming soon" to live. It is a full, ordered, click-by-click setup path for a first WooCommerce store, not a design or copywriting guide.

## 2. Principles

1. Pick the page builder before you build anything, and pick Elementor over the WordPress block editor. Condition: this applies specifically to the Astra Starter Templates import flow, where the choice is made once and determines which editor every later page edit uses. Evidence: presenter's direct instruction, repeated with emphasis ("really, really important step"). [b6dd763aa701] [a4bfc0ed6c74]
2. Start from a template, then customize, instead of building from scratch. Condition: applies when speed to a working layout matters more than a fully bespoke design. Evidence: presenter's stated workflow ("it's so much easier, and I do this with all my websites"), not a tested comparison against from-scratch builds. [a4bfc0ed6c74] [18c613fbcfcf]
3. Seed real products before final content polish. Condition: implicit in the source's own order — products and categories are set up before the homepage's "trending products" shortcode is expected to populate, and before upsell/cross-sell fields have anything to link to. Evidence: the trending-products section is shown as an empty gray bar until products exist; upsells/cross-sells fields are shown empty because no other products exist yet. [774893c987c2] [487c7ec1c105]
4. Device-specific sections are a layout escape hatch, not the default. Condition: use only when a section behaves badly on a device (e.g., background video not autoplaying on mobile), not as a routine way to build every section twice. Evidence: presenter duplicates only the one section that broke (the video hero), not the whole page; the card layer itself flags this as a maintenance cost. [019a055e9ce8] [ae2ae53144f1]
5. Test-mode payment gateways must be explicitly switched to Live, and re-verified. Condition: applies to every gateway connected (Stripe and PayPal both shown). Evidence: presenter explicitly clicks the mode toggle and re-checks the connection test result reads "Live" before saving — framed as a step that is easy to silently skip. [bb0bfd9cf533] [8408a99f2223]
6. A free-shipping threshold is a margin decision, not a copy-paste number. Condition: whenever offering free shipping over a minimum spend. Evidence: the card layer explicitly marks the source's $100 example as illustrative, not a benchmark, and warns a threshold below typical basket size gives away margin with no behavior change; the source itself gives no basket-size reasoning, only the mechanic. [e0349a2e584a] [01aafe27763f]
7. Coupon abuse controls need both a discount type and a redemption cap or they can be stacked. Condition: applies to any promotional coupon, most concretely a first-purchase welcome coupon. Evidence: presenter sets "usage limit per user: 1" specifically to stop repeat use by the same buyer. [85bfef85b9bf] [60a02cc9a78e]
8. Header and footer live in the theme's Customize screen, not in Elementor. Condition: true for the Astra theme in this walkthrough; anything visually "between" header and footer is Elementor's domain. Evidence: presenter states this distinction directly when introducing the Customize panel. [86b429e07dcd]
9. A responsive-looking template is not automatically responsive per element. Condition: after any template import or content swap, check mobile/tablet explicitly — the source shows a default video hero rendering broken (a gray gap) on mobile despite Astra/Elementor being marketed as responsive. Evidence: presenter's own screen-recorded discovery of the broken mobile hero, mid-tutorial. [b972166dd616] [ae2ae53144f1]
10. Don't flip a store to Live before checkout, payments and shipping are tested. Condition: final go-live step. Evidence: card-layer caveat built directly from the source's own step order (payments and shipping are configured and tested before the coming-soon toggle is touched). [978ff56aaae8]

## 3. Procedures

### A. Hosting, domain and WordPress install
1. Buy hosting and a domain together through a host (source uses Hostinger, via the presenter's affiliate link and a stated discount code). [web check: current Hostinger plans, pricing and any coupon code — presenter's numbers are point-in-time and affiliate-linked]
2. Choose a plan: presenter recommends the Business plan for more sites, more storage and a free CDN, but says any plan works for this tutorial.
3. Choose a billing term: presenter's rule of thumb — 12 to 48 months; go no shorter than 12 months because "one month isn't enough to even get sales and figure out if this is worth it." Longer terms cost less per month.
4. Skip entering a domain at the hosting-plan step; add it in the dedicated domain step that follows, which the presenter says is easier.
5. Complete billing address and payment, submit, then click "Get started" → "Create a website" → "Next."
6. Select WordPress as the platform → Next.
7. Create WordPress admin login credentials (username/password) → Next.
8. Choose "Create a blank site."
9. Enter the desired domain name; if a matching top-level domain shows as included free for year 1, select it → Next → confirm contact details → "Finish registration." [web check: current free-domain-with-hosting offers]
10. Select target audience/region if asked → Next. Host then installs WordPress on the new domain (took the presenter a few minutes).
11. Note: the dashboard may show a filler/temporary domain while the real domain propagates DNS globally — this is normal and can take up to 24 hours (presenter's typical experience: a few hours). [verify UI]
12. To log back into wp-admin at any time: go to `yourdomain.com/wp-admin` and enter the credentials created in step 7. [verify UI]

### B. Theme, starter template and page builder
1. Go to Appearance → Themes → Add Theme, search "Astra," Install, then Activate. [verify UI]
2. On the Astra activation screen, click "Start building now" to launch the Starter Templates plugin.
3. Click "Let's get started," fill basic info, Continue; skip any offered Pro/paid upsell by clicking Continue.
4. Choose "Build with templates" under Classic Starter Templates.
5. Critical step: click the Back button before proceeding further, then explicitly select Elementor as the page builder (not the block editor). This choice locks in the editor for all later page building. [b6dd763aa701]
6. Filter templates by category (e.g., "Ecommerce"); templates marked "premium" are paid, others are free. Pick one, review its scrolling preview, then Continue.
7. On the features screen, confirm Elementor and WooCommerce are checked (a contact form may also be pre-included); add or skip other features as needed → Continue.
8. Fill basic profile info (e.g., experience level, who the site is for) → "I understand, let's go" → "Submit and build my site."
9. Wait for the import to finish, then click "View your website" to see the imported template, ready to customize. [a4bfc0ed6c74]

### C. Elementor basics and building a hero section from scratch
1. Vocabulary: sections (thin outlined full-width bands — any area with its own background), containers (gray dashed boxes inside a section), widgets/elements (individual pieces, marked with a pencil icon) inside containers. [674f89bdf04c]
2. To add a section: click the plus button → choose Flexbox → choose a container/column layout (e.g., two containers).
3. To make a section fill the viewport: click the section's six-dot handle → set "Minimum height" units to VH → drag the slider to 100.
4. Add a Heading widget by dragging it from the elements panel; edit text inline or in the sidebar field.
5. Center content vertically: select the container (gray dashed box) → Justify Content → Center.
6. Style text: select the widget → Style tab → Text Color; Typography → pencil icon → change font family (example: Poppins) and size; delete the size value to fall back to the theme default.
7. Duplicate an element (right-click → Duplicate) to build a subheading; adjust its Typography weight (example: 400, "a normal font") and size independently.
8. Add a Divider widget below text to visually separate content; adjust width and style (solid, curved, arrows, etc.).
9. Add a Text Editor widget for body copy; if lines feel cramped, increase Typography → Line Height.
10. Add a Button widget: set its label (example: "Buy now"), then paste the destination URL in place of the default `#` (a specific product URL once products exist).
11. Style the button (see procedure D below).
12. Style the section background (see procedure E below).
13. Preview without the editing outlines via the small arrow icon; when satisfied, click Publish to save. [674f89bdf04c]

### D. Button styling (normal vs hover)
1. Select the button widget → Style tab. Note the separate "Normal" and "Hover" sub-tabs — both must be set.
2. Normal state: set text color; set background type to Classic (solid) or Gradient, then pick a color.
3. Hover state: switch to the Hover tab; set a visibly different text color and background color so shoppers can tell the button is interactive.
4. Optional: set a hover animation (example used: "Grow").
5. Border Radius: 0 = square corners; higher values move toward a fully rounded/circular shape. Presenter's example lands mid-range (~15).
6. Padding: increasing padding increases button size. Values are linked by default (top/bottom/left/right move together) — click the link icon to unlink them, then set left/right independently from top/bottom (presenter's example: 32 left/right — actually applied 15 top and 15 bottom in his final pass; treat exact numbers as illustrative, not a rule). [92302015d2d5]

### E. Section backgrounds, including video hero
1. Select the section's six-dot handle → Style tab → Background Type: Classic (solid color), Gradient (pick two colors, set angle and feather), or Video.
2. For a video background: host the video (presenter used an unlisted YouTube upload) and paste its link into the Video tab's URL field.
3. After adding a video or dark background, re-check every overlaid text element's color — presenter changes all headline/body text to white so it stays legible over the video.
4. If the video does not render well on a device (commonly mobile), do not force-play it — build a device-specific alternative instead (see procedure L, Responsive design). [b972166dd616]

### F. Adding a new page (e.g., About/Our Story)
1. Pages → Add Page → give it a title → "Edit with Elementor."
2. Build the page the same way as the homepage (procedure C).
3. To remove the page title bar: click "Page settings" → "Hide title."
4. Publish, then exit to WordPress via the WordPress logo icon in the Elementor top bar. [674f89bdf04c]

### G. Header, footer, logo and navigation menu (theme Customize screen, not Elementor)
1. Open "Customize" from the admin bar — this is Astra's settings for header/footer; everything between them is Elementor's domain. [86b429e07dcd]
2. Logo: hover the pencil icon on the logo → Logo section → untoggle the separate "transparent logo" option so one logo is used sitewide → "Change logo" → upload a transparent PNG → "Skip cropping" (cropping can cut the image) → adjust "Logo width" down if it renders oversized.
3. Site title: set it here — this is what shows in the browser tab.
4. Transparent header: enable it "on the complete website," then use "Disable on" to uncheck WooCommerce product pages if you want the identical header there too (so PDPs don't get a second, different header).
5. Header background: Design → Primary Header → pick a color (example: black) → drag the opacity slider down (example: about half) for a translucent header → Publish.
6. Navigation menu: hover the pencil icon → "Configure menu" → Primary Menu → "Edit menu" → "Add items" (Pages, Custom Links, Posts, Products, product categories/tags all selectable) → drag items to reorder, or drag one under another to create a dropdown sub-item.
7. Menu colors: Back → Header → Transparent Header → Design → Menu Color → set the normal text/link color and a distinct hover color (example: purple) to match brand → Publish. [verify UI — Astra Customizer panel names/paths change between versions]

### H. Product categories
1. Products → Categories. Delete any demo categories that came with the imported template (example in source: "Indoor plants").
2. Add new category: enter a Name; set the Slug (what appears in the URL) to something simple and lowercase; optionally set a Parent category to nest related categories (example: "Wireless headphones" and "Earbuds" under a parent "Headphones"); description and thumbnail can be skipped for now.
3. Repeat for each top-level category needed. [774893c987c2]

### I. Cleaning up demo products
1. Products → All Products → select all demo products → Bulk actions → "Move to trash" → Apply.
2. Go to Trash → empty it.
3. With the catalog empty, "Add product" will prompt for a product type: Physical (shipped), Variable (has options like color/size), or Grouped (a bundle sold as one item). [37e739ed2006]

### J. Adding a simple/variable product (full field walkthrough)
1. Products → Add Product. Choose product type (Variable used in the source's worked example).
2. Enter Product name.
3. Optional: use an AI chat tool to draft title/description by describing the product and a tone of voice, or write it manually. Long "Product description" = full sales copy; separate "short description" field = the summary shown near price/button. [needs brand data: actual product copy, tone]
4. Product Data → General: set SKU (custom stock-keeping code) and, only if a real barcode exists, UPC/GTIN (obtainable via gs1.com) — skip for placeholder/fake products.
5. Inventory: tick "Track stock quantity," enter units on hand (example: 200); set Backorders to "Do not allow" if you don't want to sell what can't be shipped; set a Low stock threshold (example: 10) to trigger "low stock, order soon" messaging.
6. Shipping tab: enter weight and dimensions for the entire package (this is what shipping-rate/label calculations use); a Shipping class can be set once created (not covered in depth here).
7. Linked Products tab: Upsells = a higher-value alternative shown on the PDP; Cross-sells = related items shown in the cart near checkout. Both require the target products to already exist. [487c7ec1c105]
8. Attributes tab (for variable products): add an attribute (example: Color); enter its values separated by the `|` symbol (example: `white|blue|pink|green`); tick "Use for variations"; Save attributes.
9. Variations tab: click "Generate variations" (confirm the prompt) to auto-create one row per value combination, rather than adding rows manually.
10. Edit each generated variation individually: set its own SKU (example pattern: `kova-echo-white`), Regular price and Sale price (sale price displays struck-through against the regular price), thumbnail image, and — if managing stock per variation — "Manage stock" plus its own quantity and low-stock threshold.
11. Set the main Product Image (shown before a shopper picks a variation) and add Product Gallery images (multiple files can be uploaded at once).
12. Assign the product to its Category (and uncheck "Uncategorized"); add Tags (brand name, product name, etc.) to aid on-site search.
13. Advanced tab: optional Purchase note shown after buying; leave Menu order at 0 unless manual sorting is needed; reviews can be toggled off if unwanted (presenter leaves them on).
14. Publish, then "Preview changes" and click through each variation option to confirm price, thumbnail and availability swap correctly.
15. To add more products fast: duplicate an existing, fully configured product and edit only what changes, rather than rebuilding every field. [6131e524a00d] [74c23b17ca3a] [cbae7d9daa4d] [37e739ed2006]

### K. Payments: Stripe and PayPal
1. Plugins → Add Plugin → search "Stripe" → find "Payment Plugins for Stripe WooCommerce" → Install → Activate. [web check: current recommended/maintained plugin — source itself flags vendor names can change]
2. Repeat: Plugins → Add Plugin → search "PayPal" → find "Payment Plugins for PayPal WooCommerce" → Install → Activate.
3. WooCommerce → Stripe (by Payment Plugins) → Settings; dismiss any onboarding prompt if shown; click "Click to connect"; provide business details, connect a bank account, set the credit-card statement descriptor; Agree and submit.
4. Once connected, change the mode from Test to Live, click "Connection test," confirm it reports success and the mode reads Live, then Save.
5. WooCommerce → PayPal (by Payment Plugins) → Settings → "Click to connect" → enter PayPal account info → Save.
6. Go to WooCommerce → Settings → Payments; confirm the Stripe/credit-card gateway is active; scroll to PayPal — it may show as inactive by default — click Enable.
7. Verify end to end: add a product to the cart → View cart → Proceed to checkout → confirm both the card fields and the PayPal option render. [bb0bfd9cf533] [8408a99f2223]

### L. Shipping zones
1. WooCommerce → Settings → Shipping → "Add zone."
2. Name the zone (example: United States) and set Zone regions.
3. "Add shipping method" → Flat rate: name it (example: "Standard rate"), set Taxable status (example: none), set a Cost (example: $10) → Create and save.
4. "Add shipping method" again → Free shipping → Continue: set the requirement to a Minimum order amount (example: $100). Leave "Apply minimum order rule before coupon" unchecked if the threshold should be judged after coupon discounts are applied.
5. Drag the Free Shipping method above the Flat Rate method within the zone, so qualifying carts get it automatically.
6. Save changes; test with a cart just below and just above the threshold to confirm the correct method wins. [e0349a2e584a] [01aafe27763f]
7. Repeat with additional zones for other countries/regions as needed; local pickup exists as an option but the source calls it rarely used.

### M. Welcome/promo coupon
1. Marketing → Coupons → create new coupon; give it a recognizable code (example: `welcome10`).
2. Discount type: change from the default "Fixed cart discount" to "Percentage discount"; enter the rate (example: 10).
3. Optional: tick the free-shipping box to bundle free shipping into the coupon (skipped for the welcome-coupon example).
4. Optional: set an expiration date via the calendar.
5. Usage restriction tab: set minimum/maximum spend if desired; tick "prevent coupon stacking" if customers should not combine codes; optionally exclude sale items; optionally scope to specific products/categories/brands (example: applied to all products).
6. Usage limits tab: set "Usage limit per user" to 1 to stop repeat redemption by the same shopper; optionally cap total redemptions.
7. Publish. Test on the storefront: add a product to cart → View cart → enter the code → Apply coupon → confirm the discount amount matches (source example: 10% off removed about $8). [85bfef85b9bf] [60a02cc9a78e]

### N. Mobile/tablet responsiveness in Elementor
1. Open "Edit with Elementor" → use the desktop/tablet/phone icons at the bottom of the panel to preview each breakpoint.
2. If a section breaks on a device (example: a video background renders as a gray gap on mobile because it won't autoplay), fix it with a device-specific duplicate rather than forcing the original to work everywhere:
   a. Duplicate the section.
   b. On the duplicate meant for mobile: select it → Advanced tab → Responsive → set "Hide on tablet" and "Hide on desktop" (leave it visible on mobile).
   c. On the original section: Advanced → Responsive → set "Hide on mobile" (leave tablet/desktop visible).
   d. Rebuild the mobile duplicate's content for the smaller screen — e.g., remove the unplayable video, switch background to Gradient, add a static Image widget instead.
3. Padding: Advanced tab → Padding controls show a small device icon next to each field when that value is scoped to the current device only; a field without the icon changes the value globally across all breakpoints. Set global values first, device-specific overrides second, to avoid one overwriting the other.
4. Individual widgets (buttons, headings, images) also carry their own per-device Style controls (e.g., Position) — check for the device icon before changing, then the change applies to only that breakpoint (example: centering a button on mobile only, leaving its desktop left-alignment untouched).
5. Repeat the check for tablet, not just mobile.
6. Publish, then use the eyeball/preview icon to confirm real rendering before moving on. [019a055e9ce8] [ae2ae53144f1] [9849b1ae9fc7] [d34b4f9dd817]

### O. Product-page (PDP) spacing and buttons via Customize
1. Open a single product page → Customize (this reaches WooCommerce's Single Product theme settings, separate from Elementor).
2. Design panel: unlink padding values, set top padding (example: 120px) so content clears a sticky header.
3. Sticky add-to-cart button: set its background and hover colors in the same Design panel (a page refresh may be needed to see the update).
4. Global button colors: Global → Buttons → set background/hover → Publish → refresh to confirm.
5. General → Single Product: edit the shipping-note text (e.g., replace "free shipping" wording) if your terms differ.
6. Back in the product editor's Advanced tab: add a Purchase note if desired; leave Menu order at 0 unless sorting is needed. [c471d0cba973]

### P. Product image sizing (catalog grids)
1. If thumbnails look grainy/blurry in grid/category views, open Customize → (theme's) Product images settings → set explicit dimensions (example: 900×600) → Publish. [37e739ed2006]

### Q. Go live
1. Confirm all page building, responsive fixes and content replacement are done and Published.
2. Preview with the eyeball icon and check desktop and mobile.
3. Confirm payments (Stripe + PayPal, Live mode, tested), shipping zones and any coupons are configured and tested before proceeding — do not skip this check.
4. Locate the store's "Coming Soon" indicator/notice, open its setting, switch it to "Live," and save.
5. Verify from a logged-out/incognito browser that product pages and checkout are publicly reachable — preview inside the editor is not proof the public site works. [978ff56aaae8]

## 4. Rules, thresholds and numbers

| Rule / value | Number | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Hosting billing term | 12–48 months, "no less than 12" | Choosing a Hostinger term for a new store | Presenter's opinion: 1 month isn't enough to get sales and judge fit | — (procedure A) |
| Hostinger price shown | $3.38/mo (sale) or "~$4/mo" off-sale, on 12-month term | Point-in-time, tied to a Black Friday-type sale | Presenter's screen at time of recording | [web check: current pricing] |
| Domain propagation | Up to 24 hours, typically "a few hours" | After purchasing a new domain via the host | Presenter's stated typical experience | — (procedure A) |
| Free-shipping threshold example | $100 minimum order | Example only, for a free-shipping method | Presenter's tutorial example, explicitly not a benchmark | [e0349a2e584a] [01aafe27763f] |
| Flat-rate shipping example | $10 | Example only, for a standard flat-rate method | Presenter's tutorial example | [01aafe27763f] |
| Welcome coupon discount | 10% | Example only | Presenter's tutorial example ("illustrative, not a recommended rate") | [85bfef85b9bf] [60a02cc9a78e] |
| Coupon usage limit per user | 1 | Applies to a first-purchase/welcome coupon | Presenter's stated anti-abuse setting | [85bfef85b9bf] [60a02cc9a78e] |
| Low stock threshold example | 10 units | Example only, per product/variation | Presenter's tutorial example | [cbae7d9daa4d] [74c23b17ca3a] |
| Product image size fix | 900×600 px | When catalog thumbnails render blurry | Presenter's tutorial example, not a measured optimum | [37e739ed2006] |
| PDP top padding fix | 120 px | When content is hidden behind a sticky header | Presenter's tutorial example | [c471d0cba973] |
| Button border radius | ~15 (mid-range) | Styling choice, 0 = square, higher = circular | Presenter's stylistic choice | [92302015d2d5] |
| Domain price example | ~$16/year for a `.com` | Point-in-time example | Presenter's screen at time of recording | [web check: current domain pricing] |
| Section "fill viewport" height | 100 (units = VH) | Making a section fill the screen | Elementor mechanic, not a design rule | [674f89bdf04c] |

## 5. Diagnostics and checks

| What to check | How | Good | Bad | Fix |
|---|---|---|---|---|
| Payment gateway mode | Open Stripe/PayPal settings, read the mode indicator | Reads "Live," connection test succeeds | Reads "Test," or connection test fails | Flip mode toggle to Live; re-run connection test; do a live test transaction before launch [bb0bfd9cf533] |
| Coupon abuse control | Apply the code twice as the same test customer | Second attempt is blocked | Second attempt succeeds | Confirm "Usage limit per user" is set to 1 (or intended value) and saved [85bfef85b9bf] |
| Free-shipping threshold | Add items to reach just under, then just over the threshold | Below threshold charges shipping; at/above shows free | Free shipping applies too early or never | Recheck the Minimum order amount field and its position above/below the flat-rate method in the zone [e0349a2e584a] |
| Mobile hero rendering | Switch Elementor to mobile/tablet preview after any background-media change | Section renders cleanly, no autoplay gap | Gray gap or broken layout (common with background video) | Duplicate the section and build a mobile-only version per procedure N [b972166dd616] [ae2ae53144f1] |
| Responsive edit scope | Look for the small device icon beside a padding/position control before editing | Icon present = edit is scoped to current device only | Icon absent = edit is global and will overwrite other breakpoints | Set global values first, then device-specific overrides after [9849b1ae9fc7] [d34b4f9dd817] |
| Demo content residue | Browse Products, Categories after template import | Only your own products/categories remain | Template demo items still present (e.g., "Indoor plants") | Bulk-trash and empty trash before adding real catalog [37e739ed2006] |
| Variation completeness | Open each generated variation row | SKU, price and stock filled per row | Blank rows left after "Generate variations" | Manually edit every generated variation before publishing [6131e524a00d] |
| Public reachability at launch | Visit the site logged out / in incognito | Store pages and checkout load for an anonymous visitor | Store still shows "Coming Soon" or password-protected | Complete the coming-soon → Live toggle and save [978ff56aaae8] |
| Thumbnail sharpness | View category/grid pages | Product images render crisp | Images look grainy/blurry in grids | Increase the theme's product image dimensions (example: 900×600) [37e739ed2006] |

## 6. Tools, settings and named features

- **Hostinger** — hosting + domain registrar used in the walkthrough; presenter is an affiliate with a stated discount link and coupon code. [web check: current plans/pricing/coupon] [verify UI]
- **WordPress** — CMS platform; installed through the host's one-click flow.
- **WooCommerce** — ecommerce plugin providing products, orders, shipping, coupons, tax settings; bundled into the Starter Templates ecommerce import.
- **Astra** — WordPress theme installed via Appearance → Themes → Add Theme. [verify UI]
- **Astra Starter Templates plugin** — imports a full pre-built site (pages, demo content, chosen page builder) after theme activation. [verify UI]
- **Elementor** — drag-and-drop page builder; explicitly chosen over the WordPress block editor during template import. Vocabulary: Sections → Containers → Widgets. [verify UI]
- **Payment Plugins for Stripe WooCommerce** and **Payment Plugins for PayPal WooCommerce** — named gateway plugins; source flags that vendor names/plugins in this space can change — verify current maintained options. [web check]
- **Customize** (WordPress Customizer, Astra theme options) — controls header, footer, logo, transparent header, menu, Single Product page design, global button colors, and product image dimensions — separate from Elementor. [verify UI]
- **Marketing → Coupons** (WooCommerce) — coupon creation screen (discount type, usage restriction, usage limits tabs).
- **gs1.com** — mentioned as the source for real UPC/GTIN barcodes, only relevant for real (non-placeholder) products.
- **Canva** — mentioned only in the companion Shopify/Claude Code source, not this one (do not conflate).

## 7. Examples and case results

- Worked example throughout: an electronics store ("Kova Echo" headphones, plus a computer mouse), domain `kovaenology.com`. This is a live demo build for the tutorial, not a store with sales results. All prices, thresholds and settings shown ($299.99 regular / $199.99 sale headphones; $10 flat shipping; $100 free-shipping threshold; 10% welcome coupon; SKU pattern `kova-echo-white`) are illustrative values from this single demo, not benchmarks. [multiple cards, see section 3]
- Coupon test result: applying the 10% "welcome10" code removed "about $8" from a cart — presented only to confirm the mechanic works, not as a pricing recommendation. [60a02cc9a78e]

## 8. Mistakes the source warns about

- Choosing the WordPress block editor instead of Elementor during template import — locks you into the wrong editor for later work. [b6dd763aa701] [a4bfc0ed6c74]
- Leaving generated product variations blank after "Generate variations" — rows are created empty and can ship live with missing price or SKU. [6131e524a00d]
- Forgetting to switch a payment gateway from Test to Live — checkout can appear to work while no money is actually collected. [bb0bfd9cf533] [8408a99f2223]
- Setting a coupon's percentage discount without a per-user usage limit — the same buyer can reuse it repeatedly. [85bfef85b9bf] [60a02cc9a78e]
- Editing a responsive control without checking for the device-scope icon — an intended mobile-only tweak can silently overwrite desktop and tablet too. [9849b1ae9fc7] [d34b4f9dd817]
- Leaving template demo products/categories in place (e.g., "Indoor plants") when launching a different kind of store. [37e739ed2006]
- Duplicating a configured product for speed without scrubbing over the old images, descriptions and variations first. [37e739ed2006]
- Assuming an imported template is responsive everywhere without checking each breakpoint — the source's own video-background hero broke on mobile despite being a "responsive" template. [b972166dd616] [ae2ae53144f1]
- Flipping "Coming Soon" to "Live" before payments, shipping and checkout are actually tested. [978ff56aaae8]
- Trusting the in-editor preview as proof the public site works — it is not the same as an incognito/logged-out visit. [978ff56aaae8]

## 9. Caveats, conflicts and what is missing

- **Affiliate conflict of interest**: the presenter recommends Hostinger through his own affiliate/discount link and a personal coupon code. Treat the host recommendation and its pricing as promotional, not neutral advice, and re-check current pricing and alternatives independently. [web check: Hostinger pricing; consider other hosts] [8408a99f2223 caveat layer]
- **No SEO, analytics, backups, staging or security setup** is covered. The source is scoped to visual build + core commerce mechanics only (payments, shipping, coupons, responsiveness, launch toggle) — nothing on tracking pixels, sitemap, SSL specifics, or post-launch maintenance.
- **No copywriting or conversion-strategy guidance** — product descriptions are drafted informally ("ask GPT," "paste in what I want") with no framework; this source explicitly hands that job elsewhere (07-LPG per its own routing header).
- **No tax-setup detail**: WooCommerce tax service/regions are not walked through in this transcript at all (unlike the companion Shopify source, which does cover it) — this is a gap, not an omission to fill in from elsewhere without a card.
- **Legal/policy pages** (refund, privacy, terms, shipping policy) are not covered in this source — also a gap versus the companion Shopify source.
- **Version drift risk is explicit and high**: the source itself instructs skipping tutorials older than ~18 months because WordPress/Elementor/Astra interfaces change frequently, and every click-path card in this file inherits a `[verify UI]` caution.
- **Numbers are illustrative, not tested**: shipping thresholds ($100), flat rate ($10), coupon depth (10%), low-stock threshold (10 units), image size (900×600), and PDP padding (120px) are all this presenter's one-time choices for a demo store — no data or reasoning is given for why those specific values were chosen. Do not present them as benchmarks.
- **No conflict with other sources found** within this file — it does not cite or contradict any other named source in the library; any apparent overlap with the companion "Shopify + Claude Code" source in the same folder is a different platform (WordPress/WooCommerce vs. Shopify) and should not be merged as if interchangeable.

## 10. Card index

- b6dd763aa701 — WordPress + WooCommerce baseline stack with Astra and Elementor
- 019a055e9ce8 — Creating mobile-specific layouts with Elementor responsive toggles
- 6131e524a00d — Building WooCommerce variable products with color/size variations
- bb0bfd9cf533 — Connecting Stripe and PayPal payments in WooCommerce
- e0349a2e584a — Configuring shipping zones with flat rate vs free-shipping thresholds
- 85bfef85b9bf — Setting up a first-purchase welcome coupon with usage controls
- 74c23b17ca3a — Set up WooCommerce variable products with generated variations
- cbae7d9daa4d — Product data fields that drive PDP content: SKU, stock, weight
- 8408a99f2223 — Configure Stripe and PayPal for WooCommerce and switch to live
- 01aafe27763f — Shipping zones, flat rate and free-shipping thresholds
- 60a02cc9a78e — Welcome coupon setup: percentage, usage limits, exclusions
- a4bfc0ed6c74 — Use a starter template, then customize instead of building from scratch
- 674f89bdf04c — Elementor structure: sections, containers and widgets
- 92302015d2d5 — Style buttons for visibility: normal vs hover states, padding, radius
- b972166dd616 — Video and image hero sections on the homepage
- 86b429e07dcd — Header and footer are theme settings, not Elementor
- 774893c987c2 — Organize the catalog with product categories and parent/child structure
- 487c7ec1c105 — Upsells and cross-sells in WooCommerce linked products
- 37e739ed2006 — Clean up demo products before adding your own catalog
- ae2ae53144f1 — Responsive design: serve different sections per device in Elementor
- c471d0cba973 — Single product page spacing and button styling via Customize
- 9849b1ae9fc7 — Edit Elementor sections with device-specific padding
- d34b4f9dd817 — Center misaligned Elementor widgets per breakpoint
- 978ff56aaae8 — Launch a WooCommerce store by switching from coming-soon to live
- 18c613fbcfcf — Customise an imported template by replacing images, colours and text
