# Shopify Tutorial for Beginners 2026 - Full Store Setup Guide

source_id: 1W04kIr1BnMuNtbN7gatR5GZ67V3eiTKG  |  folder: 05-SET-store-setup  |  cards: 8  |  words: 7,718  |  type: video tutorial transcript

credibility: A YouTube creator named Simon narrates a live, start-to-finish walkthrough of building one demo store ("Rogue Apparel"-style) in the Shopify admin. No credentials, client roster, sales figures or case studies are given. The only evidence is what the presenter shows happening on his own screen while building the demo store. The video description carries a referral/affiliate signup link for Shopify's extended trial, which the presenter promotes twice (start and end of video) — treat trial-offer claims as an affiliate recommendation, not neutral advice.

date signals: Video is dated 2026 in its title. It shows the Horizon theme as Shopify's current default (replacing older defaults), a native AI theme generator, a native AI product-description helper, and a native AI custom-section ("block") generator — all recent Shopify features, which dates this to a fairly current Shopify admin build. The specific trial structure described (3 days free, then 3 months at $1/month) is a promo term that Shopify changes over time. `[web check: current Shopify trial and pricing terms]`

## 1. What this source is for

A linear, beginner-facing walkthrough for taking a brand-new Shopify account from signup to a live, unlocked storefront: claiming a trial, picking a plan, choosing and lightly customizing a theme, adding products and collections, setting shipping rates, generating legal policy pages, turning on payments, connecting a domain, and removing the storefront password. It is a "how to click through the admin" guide, not a strategy or conversion-optimization guide. Note: about half the transcript (theme browsing, hero/section editing, colors, typography, navigation, footer styling, AI block generator) is storefront/theme-editor work that the folder scope note for this library assigns to 07-LPG rather than 05-SET; it is documented in full here because it is inseparable from this one source's walkthrough, but a 05-SET folder playbook should draw primarily on the backend/account/product/shipping/policy/domain/payments sections below.

## 2. Principles

1. Enter payment details and pick a plan within the first 3 days of signup, even if Shopify lets you skip that step, or you risk losing the extended trial's discounted period. Condition: only relevant if you signed up via the extended-trial promo. Evidence: presenter's own account walkthrough, no source cited for the deadline mechanics. `[web check: current trial terms]`
2. Start on the cheapest ("Basic") plan when a store is new; the only meaningful difference between Shopify's plans, per the presenter, is that higher plans charge a lower per-sale transaction fee. Upgrade later once sales volume justifies it. Condition: applies to a store with no consistent revenue yet. Evidence: presenter's opinion, not sourced to Shopify documentation. `[web check: current plan tiers and fees]`
3. The Horizon theme (Shopify's shipped default) is a safe default choice because it works for most store types, is one of the most-used themes, and gets Shopify's newest features first (e.g. AI-generated custom sections). Condition: applies when you have not found a paid/free theme you prefer more. Evidence: presenter's stated preference after trying the theme store and the AI theme generator; not a controlled comparison.
4. Design on desktop, but check the mobile view regularly, because most shoppers shop on mobile and Shopify auto-adapts most layouts. Condition: applies throughout theme/storefront editing. Evidence: presenter's stated reasoning, no data cited.
5. Populate a product's shipping weight and volume fields only if your shipping rates are actually calculated by weight or volume; leave them blank if you charge a flat rate, since they do nothing on their own. Condition: depends on which rate type is active in Settings > Shipping. Card: [9cf73ec552f2].
6. Decide "continue selling when out of stock" based on whether you can genuinely source/fulfil after the sale (e.g. dropshipping can leave it on; a store with fixed physical stock should leave it off so the item shows sold out at zero). Card: [aa3eb044920e].
7. Manual collections are not fed automatically; membership is edited by hand, so every new product needs to be manually added to its collection(s) after creation. Card: [343ec6b3bbe4].
8. Delete Shopify's default shipping zone/rates before building your own; the defaults are weight-based and tied to a $50+ free-shipping threshold that may not match your real fulfilment costs. Card: [c2dc1a7de78b].
9. A store is not actually visible to customers just because it is built; the storefront stays password-protected until you explicitly remove the password in Online Store settings.

## 3. Procedures

Steps are given in the order the source performs them. `[verify UI]` marks every menu label, button name or admin location, since Shopify's admin changes over time.

### A. Signup and plan (backend / 05-SET scope)
1. Go to the trial link in the video description (an affiliate link) to land on the signup page. **Affiliate recommendation** — this is a monetized referral link, not a neutral feature. `[web check: current trial mechanics]`
2. Enter email, click Continue, choose a password, click "Create Shopify account." `[verify UI]`
3. On the payment-details step, you may click Skip and add details later, but enter them within the first 3 days to keep the extended trial. Presenter clicks "Subscribe for $1." `[verify UI]` `[web check: current trial price]`
4. Choose a plan. Presenter selects "Basic" and clicks "Try Basic." `[verify UI]` `[web check: current plan names/prices]`
5. Enter business address, or a personal address if you have no registered business yet, click Continue.
6. Skip Shopify's business-questionnaire step (presenter says it does not change what you get in the backend).
7. Land in the Shopify dashboard (the "back end"). A built-in AI assistant panel appears on the right; presenter closes it for the tutorial but notes it can be asked questions at any time. `[verify UI]`

### B. Theme selection (storefront/theme-editor scope — cross-ref 07-LPG)
8. Go to Online Store > Themes. `[verify UI]` The installed default is the Horizon theme.
9. Click "Visit theme store" to browse all available themes in a new tab. Use the "Free" filter to see only free themes. `[verify UI]`
10. Click a theme > "View demo" to browse its demo store, check product pages, and check the mobile view.
11. If you like a theme, click "Try theme" to install it onto your store (does not yet activate it).
12. To activate an installed theme: under "Theme library," click Publish, then confirm. `[verify UI]`
13. Alternative: use Shopify's AI theme generator (scroll down on the Themes page). Type a keyword/phrase describing your store and click "Generate themes" to get 3 custom-made theme options. Presenter tries this but prefers a pre-made theme.
14. Presenter reverts to the Horizon theme (Publish > confirm) as the final choice, citing broad compatibility, popularity, and first access to new features like AI-generated custom sections.

### C. Store/theme editor basics (storefront/theme-editor scope — cross-ref 07-LPG)
15. Click "Edit theme" to open the store editor. `[verify UI]`
16. Right panel = live preview of the storefront; left panel = structure overview for the current page (header, page content blocks, footer).
17. Switch between Desktop view and Mobile view using the toggle at top right; check both periodically.
18. Page structure, top to bottom: header (announcement bar, menu, cart icon) → page content (e.g. hero, then feature/collection sections on the homepage) → footer (email signup, policy links, social icons, store text).

### D. Hero section and logo (storefront scope)
19. Click the hero background, or click "Hero" in the section overview, to open its settings.
20. Drag and drop a hero image into the image field to replace the background; a second image field is available for a two-image hero layout.
21. Change Height from Medium to Large to enlarge the section (example adjustment).
22. Change Position from Bottom to Center to center the text/button block.
23. Click the hero text to edit it directly; click the button to edit its label the same way.
24. Add a logo: click the gear icon (top left) > Logo and favicon. `[verify UI]` Drag/drop the logo into the default logo field.
25. Resize the logo if needed — presenter reduces height from 36px to 30px (example value, not a rule).
26. Add a favicon (a square version of the logo) in the same panel. Click Save.
27. Preview via the "..." menu > View, and confirm the favicon shows in the browser tab.
28. Change header logo position: go to Header in the section overview > Logo position: Left to Center (example preference). Save periodically using the Save button, top right.

### E. Adding products (backend / 05-SET scope)
29. Save changes and click Exit (top left) to leave the theme editor and return to the dashboard.
30. Go to Products > Add product. `[verify UI]`
31. Enter the product Title, then the Description (or use Shopify's built-in AI description generator if unsure how to write it — the source offers this without judging output quality). Card: [900e6376b2c2].
32. Drag and drop several high-quality images; reorder them, since the first image is what shows on product and collection pages. Card: [900e6376b2c2].
33. Set the Price (example: $49).
34. Optionally set a Compare-at price (a higher reference price) so the storefront shows a strikethrough "discount." Card: [5094ffe6554 9] — see card index.
35. Under Inventory, enter current stock count. Shopify auto-decrements it per sale. Toggle "Continue selling when out of stock" ON if you can still fulfil after stock hits zero (e.g. dropshipping); leave it OFF to show a "sold out" badge at zero. Manually update the count when new stock arrives. Card: [aa3eb044920e].
36. Under Shipping, enter weight and box volume only if your shipping rates will be weight/volume-based; presenter leaves these blank because he is using flat rates. Card: [9cf73ec552f2].
37. Under Variants, add options such as size or color to generate a variant grid; a different price can be set per variant (e.g. larger sizes or premium colors) — presenter leaves this at default without testing it. Card: [b65346a1a919].
38. Leave the remaining options (including the search-engine listing fields) as default, or complete them to control how the item appears in search. Click Save.
39. Repeat product creation for each item to sell (presenter adds "a few more" beyond the first, unspecified count).

### F. Collections (backend / 05-SET scope)
40. Go to Products > Collections. `[verify UI]` Delete any unwanted default collection (e.g. a pre-made "Home page" collection): select it > "..." menu > Delete collection > confirm.
41. Click Add collection. Enter a Title (example: "Shirts"). Drag/drop a collection image, click Done.
42. Keep Collection type as Manual so you control membership by hand.
43. Under Products, click Browse, select the products for this collection, click Add, then Save.
44. Repeat for each category (presenter builds several, plus a curated "New arrivals" collection for home-page featuring). Card: [343ec6b3bbe4].

### G. Displaying collections on the homepage (storefront scope)
45. Return to Online Store > Edit theme. Products added in step E now appear automatically wherever placeholder products were.
46. To show curated collections instead of a random product grid: hover the existing "Featured collection" section and click its trash icon to delete it.
47. Click "Add section" > scroll to Collections > choose "Collection list" (grid layout). Under Collections, click Select and choose which collections to display (example: Shirts, Sweaters, Jackets). Each tile shows the collection image and name and links to that collection's page.
48. Optionally delete an unwanted header text block above the list (e.g. "Shop by collection") the same way (hover > trash icon).
49. Add a second section for a curated collection: "Add section" > Products > "Featured collection carousel." Select the target collection (example: "New arrivals"). Shoppers can scroll it via an arrow control.
50. Save changes.
51. Optional: browse "Add section" further for other layouts (more product/collection displays, text blocks, FAQs, etc.) — no specific recommendation given beyond "take some time to go through these."

### H. AI custom section generator (storefront scope)
52. Click "Add section" > Generate (top of the panel). Type a prompt describing the desired layout (example: image on one side, text on the other). Click the arrow/submit control.
53. Wait roughly a few seconds; Shopify returns a custom-coded section matching the prompt, with its own configurable options panel (same as native sections).
54. To add a feature the generated section lacks, type a follow-up instruction in the same prompt box (example: "add a feature that lets me change the image style to fill frame") and submit. Wait roughly 30 seconds for Shopify to add the new option, then use it (example: switch Image style from "Fit image" to "Fill frame").

### I. Other pages, colors, fonts, animations (storefront scope)
55. Visit Products > Default product (in the editor's page navigator) to see/edit the shared product-page layout (product info + recommended products). Presenter leaves this mostly as shipped, noting Shopify's defaults are usually already optimized.
56. Change a section's color scheme: click into the section > Options > Color scheme, and pick a numbered scheme (example: Scheme 1 = white background/black text; Scheme 5 = dark background; Scheme 4 = light blue background).
57. Edit the actual palette: gear icon > Theme settings > Colors > pick a scheme > edit individual swatches (e.g. background color) to match brand colors.
58. Set fonts: gear icon > Theme settings > Typography > choose fonts for body text, subheadings, and headings.
59. Add polish: Theme settings > Animations > example, set "Card hover effect" to Zoom so collection/product images zoom slightly on hover.

### J. Navigation menu (storefront scope)
60. Click the nav bar in the editor > Menu > Main menu > Edit (this routes to the dashboard's Content > Menus). `[verify UI]`
61. Delete default menu items. Click "Add menu item," set the link to a Collection, choose it, confirm; repeat until all desired collections are in the nav. Save.
62. Preview: hover Online Store in the dashboard nav and click the eye icon, or use the store editor's preview, to confirm links work.
63. To nest a sub-menu (for stores with subcategories, e.g. Men/Women with Shirts underneath): in the menu editor, drag a child item (e.g. "Shirts") slightly right, underneath the parent item (e.g. "Men"), then save. The storefront then shows a hover dropdown under the parent item.

### K. Header and footer cleanup (storefront scope)
64. Announcement bar: edit its text (e.g. a promo/discount message) by clicking it, or delete it entirely via the trash icon.
65. Footer email signup, text, policy links and social icons are separate blocks, each editable/removable individually.
66. Turn off "Powered by Shopify": click the relevant footer text block, toggle "Show Powered by Shopify" off.
67. Add social links: click each social icon, enter the corresponding profile URL on the left; click the X on an icon to remove it if unused.
68. Replace the placeholder store name ("My Store") shown in the footer: this is not editable in the theme editor — go to dashboard Settings > General > Store details, click the pencil icon, enter the real store name, Save. `[verify UI]`

### L. Legal policies (backend / 05-SET scope)
69. Dashboard > Settings > Policies. `[verify UI]`
70. Refund/Return policy: click "Insert template" to get Shopify's standard prefilled text; read it fully, replace bracketed placeholders with your own business details, click Publish.
71. Privacy policy: Shopify prefills this by default; review/edit the same way.
72. Terms of Service: click "Insert template," replace placeholders, click Publish.
73. Shipping policy: **no template is provided** — you must write it yourself. Source mentions using "something like ChatGPT" to draft it (flagged for curation as a low-value aside, not a vetted method). Click Publish once written.
74. Contact information: use the template or enter your own details manually, click Publish.
75. Verify: preview the store, hover the footer's "Terms and policies" area, confirm every policy link is present and opens the correct page.

### M. Pre-launch backend settings, in this order (backend / 05-SET scope)
76. Settings > General: confirm store name, billing address, currency, and default units are correct. Getting these wrong affects order records later. Card: [86354ef8e01e].
77. Settings > Payments: click "Activate Shopify Payments" to connect a bank account. Have an ID document (driver's license or passport) ready for identity verification. This enables checkout via credit card, Apple Pay, Google Pay, etc. Optionally click "Add payment method" to add an alternative (example: type "Bitcoin" to see cryptocurrency payment options); note availability varies by region. Card: [86354ef8e01e].
78. Settings > Shipping and delivery: `[verify UI]`
   a. By default there is one shipping "profile" covering all products; keep one profile for a simple store, or create separate profiles for different product types.
   b. Inspect the default zone: domestic (e.g. US) with weight-based rates and a $50+ free-shipping threshold, set by Shopify out of the box.
   c. Delete the default zone: "..." menu on the zone > Delete. The source stresses this as a necessary step before adding your own zone. Card: [c2dc1a7de78b].
   d. Click "Add shipping zone," type/select the target region (example: US, selecting all applicable states), click Done.
   e. Click "Add rate." Choose Flat rate, or a dynamic rate based on weight, volume, or carrier — presenter keeps it simple and uses flat rate.
   f. Name the rate type (Standard, Express, Economy, etc.) and set its price. Example used: Standard = $6; Express (1-2 business days) = $15. Click Done for each, then Save. Card: [c2dc1a7de78b].
79. Settings > Taxes and duties: tax obligations depend heavily on your location and where you sell; the source explicitly recommends consulting a tax professional in your region rather than following the video for tax rules. It recommends turning on Shopify's built-in tax service, which auto-calculates the tax to charge per product/customer.
80. Settings > Domains: `[verify UI]`
   a. The default `myshopify.com` address is not considered launch-ready.
   b. If you already own a domain, click "Connect existing."
   c. If not, click "Buy new domain," type the desired domain, click Search; if available, click Buy. Example price cited: about $16/year. `[web check: current Shopify domain pricing]`
   d. A purchased domain auto-connects to the store with no further setup.
81. Online Store: the store is password-protected by default. Click "Remove password" to make it publicly accessible. Click "View store" to confirm the live site loads. Card: [86354ef8e01e].

## 4. Rules, thresholds and numbers

| Rule | Number / threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Extended trial length | 3 days free, then 3 months at $1/month | Only if signed up via the promo trial link; must add payment within the first 3 days | Presenter's stated promo terms, no documentation cited `[web check]` | — |
| Plan choice for a new store | "Basic" (lowest tier) | Store has no established sales volume yet | Presenter's stated opinion: higher tiers only lower per-sale transaction fees `[web check: current tiers/fees]` | — |
| Logo resize example | 36px height reduced to 30px | Cosmetic fit on this presenter's chosen theme/logo | Example only, not a rule | — |
| Default free-shipping threshold (before deletion) | $50 and up | Shopify's shipped default zone, before you replace it | Observed default in the walkthrough | c2dc1a7de78b |
| Flat shipping rate example | Standard $6; Express $15 (1-2 business days) | Store charges flat rate, not weight/volume/carrier-based | Presenter's example prices, explicitly "not a benchmark" | c2dc1a7de78b |
| Sample product price | $49 | Example product in the walkthrough | Example, not a pricing rule | 5094ffe65549 |
| Domain price example | About $16/year | Buying a new domain through Shopify | Presenter's example `[web check: current pricing]` | — |
| AI custom-section generation time | About a few seconds (first pass); about 30 seconds (follow-up edit) | Using Shopify's AI section/block generator | Observed in the walkthrough | — |

## 5. Diagnostics and checks

- Before committing to a theme: check its demo store's product pages, general navigation, and mobile view — not just the homepage. What to look for: layout holds up on mobile, product pages look complete. No pass/fail bar given beyond "if you like it."
- Throughout theme editing: toggle to Mobile view periodically. Good = layout still reads cleanly; source gives no specific breakpoint or fault list, only "most shoppers shop on mobile."
- After setting a favicon: preview via "..." > View and check the browser tab icon renders. Bad = tab still shows a generic icon, meaning the favicon field is empty or the wrong asset was uploaded.
- After building navigation and sub-menus: use the preview eye icon and reload the live storefront to confirm dropdowns appear on hover and links route to the correct collection pages.
- After publishing legal policies: preview the storefront, hover the footer's policy area, click through each link. Good = every policy page (refund, privacy, terms, shipping, contact) opens with your business's real details, not leftover bracket placeholders. Bad = a bracket placeholder is still visible, meaning the template was not fully filled in.
- After setting shipping rates: check the buyer-facing checkout to confirm the rates and labels (Standard/Express) show as configured.
- For inventory: if "Continue selling when out of stock" is on, the check is operational, not in the admin — watch whether you can actually fulfil orders placed after stock would have hit zero; rising refund or dispute rates is the bad signal. Card: aa3eb044920e.
- Final launch check: confirm the "Remove password" step was done and "View store" loads the live site without a password gate.

## 6. Tools, settings and named features

- Shopify extended trial (3 days free + 3 months at $1/month) — reached via an **affiliate/referral link** in the video description. `[web check]`
- Shopify plans (Basic and higher tiers, differing mainly in transaction fee) `[web check: current names/prices]`
- Shopify Payments — native payment processor; requires ID verification (driver's license or passport) `[verify UI]`
- Add payment method — for alternative options such as cryptocurrency (example: Bitcoin); no specific crypto processor named; availability varies by region `[verify UI]`
- Theme Store (with a "Free" filter) and the Horizon theme (Shopify's shipped default) `[verify UI]`
- Shopify's AI theme generator — produces 3 custom themes from a text prompt `[verify UI]`
- Shopify's built-in AI assistant (dashboard panel) — mentioned, not used in the tutorial
- Shopify's AI product-description generator `[verify UI]`
- Shopify's AI custom-section ("block") generator — builds and iteratively edits a page section from a text prompt `[verify UI]`
- Store/theme editor: Hero section, Collection list (grid layout), Featured collection (carousel layout), Theme settings (Logo & favicon, Colors, Typography, Animations) `[verify UI]`
- Content > Menus — navigation menu builder with drag-to-nest sub-menus `[verify UI]`
- Settings > Policies — templates for Refund/Return, Privacy, and Terms of Service; no template for Shipping policy; Contact info template `[verify UI]`
- Settings > Shipping and delivery — profiles, zones, and rate types (flat, or dynamic by weight/volume/carrier) `[verify UI]`
- Settings > Taxes and duties — Shopify's automatic tax calculation service `[verify UI]`
- Settings > Domains — connect existing domain or buy new through Shopify `[verify UI]`
- Online Store password protection toggle (Remove password) `[verify UI]`
- ChatGPT — mentioned only as an offhand suggestion for drafting the shipping policy; not demonstrated, not endorsed with any method

## 7. Examples and case results

All figures below are from the presenter's single demo store, built live for the tutorial. None are sales results or performance outcomes — they are example settings only.
- Example product: title unspecified ("shirt"), price $49, with an optional compare-at price for a strikethrough discount. Card: 5094ffe65549.
- Example collections built: Shirts, Sweaters, Jackets, Men, Women, and a curated "New arrivals" collection (four products shown in the Shirts collection).
- Example shipping setup: one zone (US, all states), flat rates — Standard $6, Express $15 (1-2 business days). Card: c2dc1a7de78b.
- Example logo resize: 36px down to 30px.
- Example domain cost cited: about $16/year. `[web check]`
- Example AI-generated section: a prompt for "image on one side, text on the other," then a follow-up prompt to add a Fit-image/Fill-frame image-style option, delivered in about 30 seconds.

## 8. Mistakes the source warns about

- Skipping payment/plan setup past the first 3 days of the trial, which forfeits the extended $1/month period. `[web check: current terms]`
- Leaving Shopify's default shipping zone and weight-based rates in place instead of replacing them with rates that match your real fulfilment costs. Card: c2dc1a7de78b.
- Turning on "continue selling when out of stock" without the ability to actually fulfil those orders, which raises refund/dispute risk. Card: aa3eb044920e.
- Populating shipping weight/volume fields while running flat-rate shipping — those fields have no effect unless a matching dynamic rate is active, so filling them in is wasted or misleading effort. Card: 9cf73ec552f2.
- Treating manual collections as self-maintaining; they do not auto-update, so new products must be added by hand or they will be missing from category pages. Card: 343ec6b3bbe4.
- Forgetting to replace the default "My Store" footer text with the real store name (a separate step in Settings > General, not in the theme editor).
- Forgetting the "Remove password" step, leaving an otherwise finished store inaccessible to customers.
- (Card-level caveat, not the presenter's own words) Keeping a compare-at "discount" permanently raised so the sale never actually ends can undermine customer trust. Card: 5094ffe65549.

## 9. Caveats, conflicts and what is missing

- **Affiliate recommendation**: the trial-signup link promoted at the start and end of the video is a referral/affiliate link. Treat the trial-length and $1/month framing as promotional, not neutral, and verify current terms independently. `[web check]`
- The source is a single, unsponsored-looking demo build by one presenter with no named credentials, client work, or before/after sales data — every preference stated (Basic plan, Horizon theme, flat shipping, center-aligned hero, etc.) is presenter opinion, not a tested result. Flagged per source at each principle above.
- Per this library's folder split, only the account/plan setup, product data entry, collections, shipping-zone configuration, legal policies, payments, taxes, domain purchase, and password removal belong to 05-SET. The theme selection, hero/section editing, colors, typography, animations, navigation menu, and footer styling portions of this same video belong to 07-LPG (landing pages/storefront editor). Both are documented above in full because they come from one inseparable walkthrough; a 05-SET folder playbook (pass 2) should draw mainly on sections A, E, F, L and M above, and cross-reference 07-LPG for sections B, C, D, G, H, I, J, K.
- Curator "Skip" notes (from the source header data) explicitly exclude three things from being treated as guidance even though they appear in the transcript: the promotional trial link itself, using ChatGPT to write the shipping policy, and the brief taxes-dashboard overview. They are documented above for completeness but should not be cited as recommended method.
- No jurisdiction-specific tax guidance is given; the source defers entirely to "consult a tax professional," so this source cannot answer any tax-threshold question.
- No image size, pixel-count, or format guidance is given for product or hero images beyond "high quality" and "best light."
- Variant-level per-size/per-color pricing is described as available but is not actually tested in the walkthrough (default pricing is left as-is). Card: b65346a1a919.
- No competing source is present in this export to compare against, so no cross-source conflicts can be identified from this run.
- `[needs brand data: store/business name, billing address, currency, default units, product titles/descriptions/images/prices/compare-at prices, real inventory counts and restock policy, actual per-item shipping weights/box volumes if using dynamic rates, collection categories and which products belong in each, real shipping zones and carrier-based costs, tax jurisdiction and nexus, target domain name, real policy content (especially the shipping policy, which has no template) and business contact details, social media profile URLs, brand color palette and font choices, logo and favicon files]`

## 10. Card index

- 86354ef8e01ebf9b62decf5e — Shopify backend launch order
- b65346a1a91986a0de5c24de — Adding product variants for size and colour
- 5094ffe65549e9a9be80c2d6 — Compare-at price strike-through
- aa3eb044920e3e19da96ea76 — Inventory tracking and out-of-stock behaviour
- 343ec6b3bbe49011482f0cb4 — Manual collections: build category pages from a product list
- c2dc1a7de78b23dbe60f0977 — Delete default shipping zones before adding your own
- 9cf73ec552f24d169978243d — Product shipping weight and box volume
- 900e6376b2c26b45f732eba1 — Product description and imagery for the PDP
