# Claude Just Changed Shopify Forever

source_id: 1wglJbj9TYsV2mna5N3CodM3Bo1qo7VBm  |  folder: /05-SET-store-setup  |  cards: 10  |  words: 5,261  |  type: talk (single-presenter video tutorial transcript, no timestamps)

credibility: A solo, first-person screen-recorded tutorial. The presenter says he has "15 years... scaling e-commerce stores" and runs an "e-commerce academy" that sells a "Perfect Product Page" (PPP) framework workbook, which he uploads and uses mid-demo — so the tutorial doubles as a funnel into his paid product. All evidence is a single live screen-share on the presenter's own demo store ("demo 3"); there is no client data, no A/B test, no conversion measurement, and no second example. Every claim about what Claude Code "can do" is the presenter's own narration of what he just watched happen once, not a verified capability spec — treat capability claims as demonstrated-once, not guaranteed.

date signals: References "Claude Code" as a named feature, a Claude "pro account" as the plan tier that unlocks it, the Anthropic-published VS Code extension, Shopify's "Horizon" theme as the live theme, and Shopify Sidekick as an existing comparison point. The presenter says "typing is so 2025," implying recording in 2025 or very early 2026; file modified 2026-09-19. AI coding tools, IDE extensions, Claude plan names and limits, and Shopify's native AI features (Sidekick) all change on a roughly monthly cycle, so nearly every UI step below needs a live check before use. [web check: current Claude plan names/limits, current Shopify CLI install flow, current Shopify Sidekick capabilities]

## 1. What this source is for

It is a step-by-step screen-recorded walkthrough for setting up Claude Code as a local, chat-driven Shopify theme editor: install the tooling, connect it to a live store, work only on a duplicated theme, and use plain-English prompts to add trust badges, build a full product-page template from a framework document, clone a competitor's UI element from a screenshot, make sitewide theme edits, and publish safely. It targets a non-technical founder who wants developer-level theme control without hiring a developer or buying a third-party app.

## 2. Principles

1. **Claude Code can edit live Shopify theme code from plain-English prompts, without apps or a developer.** Condition: the store runs on a theme Claude Code can access locally via the Shopify CLI. This is the presenter's central claim and the whole premise of the tutorial; it is demonstrated on one demo store with no coding background shown for the presenter's own edits, but "no coding knowledge... no developer" is his framing, not an independently verified boundary. Treat it as capability shown, not capability guaranteed for every theme, every edit, or every account tier. [22f64fbbad91]
2. **Always work on a duplicated copy of the live theme, never the live theme itself.** Condition: any AI-driven or manual theme edit. This is stated as the single most important safety step in the whole workflow: prompt Claude to duplicate the live theme first, then explicitly instruct it to work only on that copy, before any editing begins. [de00dc0259ba]
3. **Claude Code is framed as more capable than Shopify's native Sidekick AI feature.** Condition: comparing AI-assisted theme editing options inside Shopify. The presenter states Sidekick can "essentially only generate sections," while Claude Code can build whole new editable blocks and entire templates. This is the presenter's own comparison, not a feature-by-feature audit of Sidekick, and Sidekick's capabilities are exactly the kind of thing that changes fast. [web check: current Shopify Sidekick feature set before repeating this comparison] [2068dc8e74a9]
4. **A generated template or component is a starting outline, not a finished, tested page.** Condition: any AI-generated template (e.g. from an uploaded framework) or cloned component. The presenter explicitly treats the output as something to refine (toggle sections, resize icons, remove duplicates) rather than ship as-is, and separately cautions that the framework itself is not proven to lift conversion just because it was coded up. [100fb168dda1] [91ef75dc529d]
5. **Give Claude one change at a time; bundling several requests in one prompt risks partial or silent failure.** Condition: any multi-part theme-edit prompt. The presenter's own bundled request (change cart icon + add icon options + add an add-to-cart animation + change notification bubble colors) got 3 of 4 parts done; the animation silently did not appear. His own inferred cause is too many instructions in one prompt, offered as a lesson learned, not a tested rule with a defined threshold (e.g. no stated max number of asks). [9e2078f63db9] [5c660bd33ab3]
6. **Heavy Claude Code use during a session can hit a usage-token limit that forces a pause.** Condition: extended theme-coding sessions. The presenter hit a "90% of your limit used" warning after several edits and reports roughly a 1-hour cooldown before continuing. Both the percentage trigger and the reset window are this presenter's one observed instance on his account and plan tier at the time of recording; Claude's plans, limits and reset windows change over time. [web check: current Claude Code usage limits and plan tiers] [af0b1c693102]
7. **Claude cannot complete OAuth-style store authentication on your behalf; you run the login command yourself.** Condition: connecting the Shopify CLI to a store for the first time. Claude generates the `shopify auth login`-style command and asks you to paste and run it in a new VS Code terminal, then pick the account, because it "breaks security restrictions" for the AI to do this step itself. [cf190b41088d]
8. **Copy a competitor's visual pattern and interaction, not their trademarked content, logo or copy.** Condition: cloning any competitor UI element via screenshot. The presenter clones True Classic's "Top Seller" badge styling and interaction pattern but rebuilds it with his own text/icon/color, consistent with the broader repo rule that competitor ads and UI are signals for layout and mood only, never material to copy outright. [91ef75dc529d]

## 3. Procedures

### 3.1 Set up the local Claude Code + Shopify environment
1. Confirm/upgrade to a Claude plan that includes Claude Code (the presenter says the free tier does not include it; he used a paid "pro" plan). [verify UI: current plan name and what tier unlocks Claude Code] [22f64fbbad91]
2. Download and install Visual Studio Code (free). [22f64fbbad91]
3. In VS Code: File > New > Open Folder. Create a new, empty folder (e.g. "Shopify editor") and open it. This folder becomes the workspace holding the theme files and the CLI/Claude connections. [22f64fbbad91]
4. Open the Extensions panel, search "Claude," and install the extension published by Anthropic specifically — the presenter warns other similarly named extensions appear in search results. [22f64fbbad91]
5. Click the Claude icon (top right of the VS Code window) to open the Claude chat panel inside the editor. The left sidebar keeps showing your files; the chat panel on the right/side is where you type prompts. [verify UI: current icon location] [22f64fbbad91]

### 3.2 Connect Claude Code to Shopify and pull your theme list
1. In the Claude chat panel, prompt: "I need to install the Shopify CLI into Visual Studio." Approve each installation prompt as it appears, checking what it says before allowing. [cf190b41088d]
2. When asked which install method, choose the NPM version. The presenter reports the Homebrew version failed for him previously — a situational preference from one person's setup, not a stated universal rule. [cf190b41088d]
3. Prompt: "Please connect to our Shopify store and give me a list of the themes on the store." [cf190b41088d]
4. When asked for the store, copy your store's URL from Shopify admin and paste it into the chat. [cf190b41088d]
5. Claude will hand you an authentication command (the presenter's example: `shopify auth login`). Open Terminal > New Terminal inside VS Code, paste the command, and press enter. [cf190b41088d]
6. Choose the correct account when prompted in the terminal; a separate browser window may open to complete login on some setups. [cf190b41088d]
7. Once authenticated, go back to the Claude chat and confirm ("authenticated"), then close the terminal if you like. [cf190b41088d]
8. Re-run or continue the "list my themes" request; confirm Claude returns your actual theme list and correctly identifies which one is currently live (the presenter's store returned 13 themes, correctly flagging "Horizon HC" as live). [cf190b41088d]

### 3.3 Duplicate the live theme and confirm the safe working copy
1. Prompt: "Can you duplicate the live theme, please?" [de00dc0259ba]
2. Immediately follow with an instruction to work only on that copy going forward (the presenter's duplicate was auto-named "copy of Horizon"). [de00dc0259ba]
3. In Shopify admin, go to Online Store > Themes and confirm the new duplicate theme appears there (created moments earlier). [de00dc0259ba]
4. Confirm in VS Code's file sidebar that the duplicate theme's files have been pulled down locally — this is what lets Claude edit code directly. [de00dc0259ba]
5. Treat the original live theme as untouchable for the rest of the session. [de00dc0259ba]

### 3.4 Add an editable trust-badge block under the buy buttons
1. In the Shopify theme editor, open the template you want to edit (the presenter uses the default product template). [2068dc8e74a9]
2. In Claude Code, prompt with the exact placement and content, e.g.: *"In the product page default template, underneath the add-to-cart button, I want to add in three icons and text that I can edit in the theme editor. One icon is going to be for shipping. The second icon is going to be for guarantees. And the third icon is going to be for returns."* [2068dc8e74a9]
3. Optionally approve "yes, allow for all edits in this session" once, so you are not asked to confirm every individual file change. [2068dc8e74a9]
4. Wait for Claude to report what it built. In the demo this took roughly 1.5 to 2 minutes and produced a delivery-truck icon, a shield icon and a refresh-arrows icon, labeled a "Product Trust Buttons" block. [2068dc8e74a9]
5. In the theme editor, refresh/reload the page and confirm the new block appears under the buy buttons, is movable/reorderable, and its icons and text are editable inline. [2068dc8e74a9]
6. Reuse this same pattern for other repeated reassurance content (e.g. payment-method icons, sizing notes). [2068dc8e74a9]

### 3.5 Generate a full product template from an uploaded framework document
1. Have a product-page framework/anatomy document ready. The presenter uploads his own paid "Perfect Product Page" (PPP) framework, which specifies a hero section, trust badges, benefits grid, outcome section, image+text block, feature highlight and social proof. [needs brand data: your own framework or page-structure spec, if you have one] [100fb168dda1]
2. Prompt: *"I now want you to create a brand new product template in this theme using the attached framework."* Attach the document to the Claude Code chat. [100fb168dda1]
3. Let Claude analyze the document and generate the template; the demo took roughly a couple of minutes and reported it had built a hero, trust badges, benefits grid, outcomes, image+text, feature highlight and social proof, then pushed it live to the duplicate theme. [100fb168dda1]
4. In Shopify admin, refresh and confirm a new template exists on the duplicate theme (the presenter's was labeled "PPP," which he self-abbreviates as also standing for "high converting"). [100fb168dda1]
5. Treat the output as a baseline outline: go through it and toggle sections on/off, resize icons, and remove any duplicated elements (the presenter turned off a redundant benefits grid that repeated content already shown elsewhere on the page). [100fb168dda1]
6. Use the theme editor's per-section settings (e.g. badge position: "above product title" vs. "over product image"; swatch style: text pill, swatch, or product-image thumbnail) to configure the template to taste — these settings appear automatically in the editor once Claude has built the section. [100fb168dda1]
7. Assign the finished template to the products where it fits, or duplicate it for testing variants. [100fb168dda1]

### 3.6 Convert variant pills to a dropdown menu
1. In the theme editor, identify the section you want changed (the presenter looks at the variant/swatch section of the PPP template). [source text]
2. In Claude Code, prompt: *"Let's add in another option to the variant section of the product details to allow for a drop-down menu for variants."* [source text]
3. Wait for Claude to locate and recode that section; the demo took roughly 2.5 minutes. [source text]
4. In the theme editor's swatch-style setting, confirm a new "dropdown" option now sits alongside the existing pill/swatch choices, and select it to verify the storefront renders a dropdown. [source text]

### 3.7 Clone a competitor's UI element from a screenshot
1. Find the specific element on a competitor's live site (the presenter's example: True Classic's "Top Seller" heart-badge on a product-variant swatch, found via Men's > Short Sleeves > Crew Necks). [91ef75dc529d]
2. Screenshot or copy that section of the competitor's page. [91ef75dc529d]
3. Paste the image into Claude Code with a scoped prompt, e.g.: *"Using the attached reference image, I now want to add a similar badge like the one 'top seller' in this reference image onto my swatches on my product page. Need to be able to add an icon, change the text and the color, but I want the styling to look exactly the same as the reference image."* [91ef75dc529d]
4. Let Claude build the component. In the demo it returned setup instructions rather than a fully wired UI: open the theme editor, navigate to a product on the PPP template, click the variant-picker block, click "Add block," add a "Swatch label," and set the swatch label's option value to match the variant's option name exactly (the presenter used "100 g" to match his own product option). [91ef75dc529d]
5. In the theme editor, set the icon/emoji, text and color on the new swatch label block to your brand. [91ef75dc529d]
6. Do not copy the competitor's brand assets, logo, product or exact copy — replicate the layout/interaction pattern only. [91ef75dc529d]

### 3.8 Make a sitewide (non-template) theme edit: cart icon and notification bubble
1. In Claude Code, scope a single sitewide request, e.g.: *"We now want to change the shopping cart icon and we want to have the ability to change the icon with some pre-selected icons... a cart, a bag, a trolley... We also want to be able to have a small animation when something is added to the cart and change the color of the number notification on that cart."* [5c660bd33ab3]
2. Wait for Claude to report where the new controls were added (in the demo: Header > Utilities in the theme editor). [5c660bd33ab3]
3. In the theme editor, go to that reported location, pick the new cart-icon style (the demo offered a bag/basket vs. a minimal trolley icon), and set the cart-count background color and cart-count number color. [5c660bd33ab3]
4. Test the add-to-cart behavior on the live storefront preview to confirm which parts of the request actually landed. In the demo, the icon swap and color changes worked but the requested add-to-cart animation did not appear — treat any multi-part sitewide request as needing this kind of verification, not an assumption that everything requested was built. [5c660bd33ab3] [9e2078f63db9]
5. If part of a bundled request fails, re-issue only the missing piece as its own single-purpose prompt rather than repeating the whole bundle. [9e2078f63db9]

### 3.9 Publish the edited theme and prepare for the next round
1. In Shopify admin, review the duplicate theme in the theme editor and confirm it looks correct before publishing. [35ef5d4ea699]
2. Click "Publish" on the edited duplicate theme. The previously live theme automatically moves to "unpublished." [35ef5d4ea699]
3. Note that theme file edits (code Claude wrote) are saved automatically to the theme's files; only in-editor content/setting changes (e.g. text you typed directly into a block, a color you picked) need an explicit save inside the editor. [35ef5d4ea699]
4. For the next round of edits, duplicate the theme that is now live (not the old working copy) so you are editing the most current version, then repeat the edit-and-publish cycle. [35ef5d4ea699]

### 3.10 Native AI prompts inside Shopify (not demonstrated in this source)
The presenter states there is a ninth chapter covering "how to use AI prompts directly within Shopify" without needing VS Code, and says he has a separate video showing it — but the transcript is cut off before this section is actually demonstrated. Nothing about setup, prompts, or results for this step is in the source text. Do not treat this as documented; source is thin on how here. [source text, no card]

## 4. Rules, thresholds and numbers

| Rule / figure | Number | Condition | Source's basis | Card |
|---|---|---|---|---|
| Claude plan needed for Claude Code | "Pro" account (free tier excluded, per presenter) | To use Claude Code for theme editing | Presenter's stated requirement at time of recording | [22f64fbbad91] |
| Themes found on presenter's demo store | 13 themes | One example store, heavily used for testing | Presenter's own demo, single instance | [cf190b41088d] |
| Trust-badge block build time | ~1.5-2 minutes | Adding 3 icons + text under add-to-cart | Presenter's single timed example | [2068dc8e74a9] |
| Full PPP template build time | "A couple of minutes" | Generating a full product template from an uploaded framework | Presenter's single timed example | [100fb168dda1] |
| Variant dropdown recode time | ~2.5 minutes | Converting swatch pills to a dropdown option | Presenter's single timed example | [source text] |
| Competitor badge clone time | Not stated precisely ("that's completed") | Cloning True Classic's badge from a screenshot | Presenter's single example, no timing given | [91ef75dc529d] |
| Whole-store edit time (presenter's headline claim) | ~30 minutes | Redesigning an entire demo store's look with Claude Code | Presenter's own unverified claim about his own demo | [source text] |
| Claude usage-limit warning trigger | "90% of your limit used" | After multiple theme edits in one extended session | Presenter's single observed instance; plan/limits change | [af0b1c693102] |
| Usage-limit cooldown | ~1 hour reset | After hitting the usage limit | Presenter's stated observation, not a published SLA | [af0b1c693102] |
| Bundled sitewide request outcome | 3 of 4 requested changes worked (icon, 2 colors); animation did not appear | Cart icon + preset options + animation + count colors requested in one prompt | Presenter's single example | [5c660bd33ab3] [9e2078f63db9] |

## 5. Diagnostics and checks

- **Is the correct extension installed?** Check: in the VS Code Extensions search for "Claude," confirm the publisher is Anthropic before installing, since similarly named extensions appear alongside it. Bad: installing a lookalike extension. [22f64fbbad91]
- **Is the CLI actually connected to your store, not just installed?** Check: ask Claude to list your store's themes and confirm it returns real theme names and correctly flags which one is live, before trusting it to edit anything. Bad: proceeding to edit without this confirmation step. [cf190b41088d]
- **Are you editing the copy, not the live theme?** Check: after asking Claude to duplicate the live theme, confirm in Shopify admin (Online Store > Themes) that a new duplicate exists, and confirm in VS Code that the duplicate's files (not the live theme's) are the ones pulled locally. Bad: skipping the "continue to work only on that theme" instruction, which risks Claude targeting the wrong theme. [de00dc0259ba]
- **Did a generated block or template actually appear, and where?** Check: before refreshing, note what is NOT there yet (the presenter explicitly clicks the buy buttons first to confirm nothing exists there); after the edit, refresh the storefront/editor and confirm the new element is present, placed correctly, and editable. Bad: assuming the AI's text report of what it built is itself proof it rendered correctly. [2068dc8e74a9]
- **Did every part of a bundled request land?** Check: test each requested behavior individually on the live preview (icon changed? color changed? animation fires on add-to-cart?). Bad: assuming a multi-part prompt fully succeeded because Claude reported success in general terms; in the demo, 3 of 4 parts worked and the animation silently did not. Fix: re-issue the missing piece as its own single, scoped prompt. [5c660bd33ab3] [9e2078f63db9]
- **Is a generated template ready to publish?** Check: walk each section (hero, trust badges, benefits grid, etc.) for duplication or redundancy against the rest of the page, and check per-section settings (badge position, swatch style) for fit. Bad: publishing the first draft output as final. [100fb168dda1]
- **Did the competitor-clone badge bind correctly to the right variant?** Check: the swatch label's option value must match the variant's option name exactly, or the badge will not attach to the intended variant. [91ef75dc529d]

## 6. Tools, settings and named features

- **Claude / Claude Code**: Anthropic's AI chatbot and its in-IDE coding feature. Requires a paid ("pro") plan per the presenter, at time of recording. Used here to write and modify Shopify theme (Liquid/JS/CSS) code directly from natural-language prompts, inside VS Code. [verify UI: current Claude plan tiers, limits, and whether Claude Code is bundled the same way] [22f64fbbad91]
- **Visual Studio Code (VS Code)**: Free code editor from Microsoft. Used as the local workspace where the Anthropic extension and Shopify CLI both run, and where theme files are pulled and edited. [22f64fbbad91]
- **Anthropic VS Code extension**: The official extension that puts a Claude chat panel inside VS Code. Presenter warns other extensions with similar names appear in the same search. [verify UI: extension name/branding can change] [22f64fbbad91]
- **Shopify CLI**: Shopify's command-line interface; the tool Claude uses under the hood to talk to a Shopify store (pull/push theme files, list themes, authenticate). Two install paths were offered in the demo: NPM (worked for the presenter) and Homebrew (failed for the presenter, on his one attempt). [verify UI: current install options and command names, e.g. `shopify auth login`] [cf190b41088d]
- **Shopify theme editor**: The native Shopify admin UI where Claude's generated blocks, templates and settings show up as editable controls (drag to reorder, per-section settings) after Claude writes the underlying code. [used throughout, e.g. 2068dc8e74a9]
- **Horizon theme**: Named as Shopify's "standard" default theme in the demo; the presenter's before/after comparison starts from an unedited Horizon store. [verify UI: whether Horizon is still Shopify's default theme] [source text]
- **Shopify Sidekick**: Shopify's own native AI feature, referenced only as a comparison point — described by the presenter as generating sections only, versus Claude Code's ability to build whole new blocks and templates. Not itself demonstrated in this source. [web check: current Sidekick capabilities before repeating this comparison] [2068dc8e74a9]
- **"Perfect Product Page" (PPP) framework document**: The presenter's own paid product-page anatomy workbook (hero, trust badges, benefits grid, outcome, image+text, feature highlight, social proof), uploaded to Claude Code as the spec for generating a template. This is promotional content for the presenter's own academy; the framework's structure is usable as a reference, but the source gives no independent evidence it improves conversion. [needs brand data: your own PDP framework or spec if you don't use this one] [100fb168dda1]
- **Whisper Flow**: A voice-to-text tool the presenter uses to dictate his prompts instead of typing ("typing is so 2025"). Incidental to the workflow, not required for it. [source text]

## 7. Examples and case results

All results below are one presenter narrating one live demo on his own test store ("demo 3"); none are independently measured or verified, and no conversion or sales data is given anywhere in the source.

- **Whole-store visual overhaul**: presenter claims a standard, unedited Horizon-theme store, after roughly 30 minutes of Claude Code editing, looked "night and day" different and would "convert a lot better" — this conversion claim is asserted, not measured. [source text]
- **Trust-badge block**: 3 icons (truck, shield, refresh arrows) plus editable text added under the buy buttons in ~1.5-2 minutes, editable and reorderable afterward. [2068dc8e74a9]
- **PPP template generation**: uploading the framework document produced a full new template (hero, trust badges, benefits grid, outcomes, image+text, feature highlight, social proof) in a couple of minutes, later trimmed by the presenter to remove a duplicated benefits grid. [100fb168dda1]
- **Variant dropdown**: converting pill/swatch variant selectors to include a dropdown option took ~2.5 minutes and worked as requested. [source text]
- **True Classic badge clone**: a screenshot of a competitor's "Top Seller" heart badge on a variant swatch was turned into an editable "Swatch label" block with custom icon, text and color, requiring the option value to match the variant name exactly. [91ef75dc529d]
- **Sitewide cart edit**: bundled request for a new cart icon (with presets), an add-to-cart animation, and cart-count color changes; icon and 2 colors landed correctly, the animation did not appear, illustrating the "one change at a time" lesson. [5c660bd33ab3] [9e2078f63db9]
- **Usage limit**: presenter hit a "90% of your limit used" warning during the session and reports a roughly 1-hour reset before resuming. [af0b1c693102]

## 8. Mistakes the source warns about

- Installing a similarly named but non-Anthropic extension instead of the official one. [22f64fbbad91]
- Editing the live theme directly instead of a duplicate — risks breaking the entire storefront. [de00dc0259ba]
- Forgetting to explicitly tell Claude to "continue to work only on that theme" after duplicating, which risks edits landing on the wrong theme. [de00dc0259ba]
- Bundling multiple distinct changes into a single prompt — parts can silently fail (the animation request) while the rest reports as done. [9e2078f63db9] [5c660bd33ab3]
- Assuming a generated template or cloned component is finished and ready to publish, rather than a first draft to prune and configure. [100fb168dda1]
- Setting a swatch label's option value to anything other than the exact variant option name, which breaks the badge's binding to that variant. [91ef75dc529d]
- Running heavy Claude Code sessions without expecting to hit a usage limit and having to pause. [af0b1c693102]
- Not testing whether every part of a multi-part request actually worked before moving on. [5c660bd33ab3]

## 9. Caveats, conflicts and what is missing

- **Every capability claim is the presenter's own narration of a single live demo on his own test store.** There is no client store, no before/after conversion data, no independent test of Claude Code's reliability across themes, and no discussion of failure modes beyond the one partial failure shown (the missing animation). Treat "you don't need any coding knowledge... you don't even need a developer" as marketing framing for the tutorial, not a verified guarantee for every store, theme or edit type.
- **This source is promotional for the presenter's own paid framework.** The PPP document used mid-demo is his own product; its structure (hero, trust badges, benefits grid, etc.) is reasonable as a reference but the source gives zero evidence that this specific framework, once coded into a template, lifts conversion. Per repo rule, mark it example, not promise.
- **The comparison to Shopify Sidekick is one person's characterization, not a feature audit**, and native Shopify AI features are exactly the kind of thing that changes monthly — verify current Sidekick capability before repeating "Sidekick can only generate sections" to a client. [web check]
- **Chapter 9 (native AI prompts inside Shopify without VS Code) is announced but never actually shown** in the source text; the transcript is cut off mid-sentence. Do not build a procedure for this step from this source — it does not exist here.
- **No cost accounting is given** beyond "upgrade to Claude Pro." There is no discussion of ongoing Claude Code usage cost, how usage-based billing interacts with heavy theme-coding sessions, or how this compares in total cost to hiring a developer or buying a theme app — a gap for anyone evaluating this against the alternative of paying for developer time or an app subscription. [needs brand data: your own cost comparison against a developer/app-based approach]
- **The "one change at a time" rule has no stated threshold** (how many instructions is too many, what kinds of requests are safe to combine) — it is a single inferred lesson from one partial failure, not a tested boundary.
- **The competitor-cloning workflow (section 3.7) sits close to a real IP/brand risk** if a user copies more than styling — the source itself only clones layout/interaction and rebuilds content, consistent with this repo's rule to use competitor UI for layout and mood only, never to copy logos, product, or exact copy. Flag this explicitly to any brand using this workflow.
- **No mention of theme performance, page speed, or backup/version-control practices** beyond "duplicate before editing" — a reader wanting speed-safe or rollback-safe AI theme editing will need to pair this with material from `/08-SPD-speed` or a proper version-control discipline; this source does not cover it.
- **Nothing here conflicts with mainstream ecommerce setup advice** on the core safety point (never edit a live theme directly) — that matches standard Shopify guidance. The claim that this removes the need for any developer for *all* theme customization is the one point that goes beyond what is normally advised, since complex theme architecture, apps requiring backend logic, and payment/checkout configuration are out of scope for this source (see the folder header: subscription/payment settings route to "05-SET (basic)", not here) and are not shown as something Claude Code handles.

## 10. Card index

1. 22f64fbbad91 — Set Up a Local AI Coding Environment for Shopify Theme Edits
2. cf190b41088d — Connect Shopify CLI and Authenticate Your Store
3. de00dc0259ba — Duplicate the Live Theme Before Any AI Editing
4. 2068dc8e74a9 — Inject an Editable Objection-Busting Trust Block Under Add to Cart
5. 100fb168dda1 — Generate a Full High-Converting Product Template from a Framework Document
6. 91ef75dc529d — Clone a Competitor Design Element via Screenshot
7. 5c660bd33ab3 — Make Global Theme Edits (Cart Icon and Notification Bubble)
8. 9e2078f63db9 — Give Claude One Change at a Time, Not a Bundle
9. af0b1c693102 — Manage Claude Usage Limits During Heavy Theme Coding
10. 35ef5d4ea699 — Publish a Claude-Edited Theme and Maintain an Up-to-Date Working Copy
