# How to Design High Converting Ecommerce Emails In Figma

source_id: 1nMppvpjSbF4ezajnM88xmM7lAuWBSWLN  |  folder: /14-EML-email-lifecycle  |  cards: 15  |  words: 7,859  |  type: talk (YouTube video transcript with a curator's summary header)

credibility: A single presenter who runs an email agency. The curator's header names the agency "Well Copy". The Omnisend discount link is "omnisend.com/max", so the presenter is likely called Max. He claims $150M in email revenue in 4 years (his own or his clients'), work with "over 200 7 to 9 figure ecommerce brands", and a $500,000 a month result for 1 brand (promoted as another video). He sells done-for-you email (strategy, copy, design, implementation, reporting) and books calls from the video. Omnisend is an affiliate or sponsor (30% off link). Evidence is his opinion plus screenshots of other brands' emails (Bite, Dr. Squatch, a brand the transcript spells "Grunes" or "Grooms", an unnamed "find your flow" email, an unnamed "$200 million a year brand"). No open rates, click rates, test results or sample sizes are given for any rule.
date signals: says "the 2026 customer" and "It is 2026". Omnisend campaign editor and Figma slice tool are shown as of that time. ButcherBox for Pets is described as a new ButcherBox branch.

Source structure note: the document has 2 parts. (a) A curator's summary header ("Topics", "Look for"). (b) The video transcript. Some header claims are not in the transcript. The biggest one: the "hidden text" deliverability hack (size 5 font, 5% line spacing, colour matched to the background) appears only in the header. The transcript never mentions it. The header also says the examples are "Gymshark and ButcherBox"; the transcript names ButcherBox but never says Gymshark. Header-only items are marked "(header only)" below.

## 1. What this source is for

It helps an operator design and ship a promotional or flow email as stacked images. It gives a 3-layer frame (copy, structure, design) to build or audit an email. It gives a fixed layout (hero with button, bridge with infographic, closing section with button, footer with navigation). It walks through a full Figma build (600 wide frame, placeholder map, buttons, background colour from the image, gradients, us-versus-them block) and a full Omnisend upload (slices, compression, padding, links, alt text, test send). It also gives a ChatGPT method to turn a competitor email into a reusable copy template.

## 2. Principles

1. **An email converts through 3 layers: copywriting, structure and graphic design.** Copy is the words (headlines, CTAs, social proof). Structure is the order and placement of sections and buttons. Design is how it looks and feels (button sizes, colours, images, flow, branding). Judge each by whether it moves a reader to buy, not by how it looks. The presenter says brands lose "tens of thousands to hundreds of thousands of dollars" by caring more about looks than performance. Evidence: his opinion. The card adds a diagnostic by layer (see section 5); that split is the card writer's, not the presenter's. [9fe5472706f8]
2. **People skim emails. They do not read them.** Copy must match the design and be scannable while pushing action. Condition: promo and consideration emails. The card notes transactional emails may need more detail. The "3-second attention span" figure is header only. [9fe5472706f8] [658d97cafe81]
3. **Name the pain in the headline, then differentiate.** Bite example: headline "What's in your toothpaste matters?", then body "we'll never include harsh chemicals, plastic tubes, or toxic fillers". Second Bite example: "Is your phone lying to you?" followed by 2 sentences of education, then the first CTA. [658d97cafe81]
4. **Sell on 3 points only, even if the product has more.** The presenter says "the human brain can really only take three things at a time". Bite lists 3 ingredients though the toothpaste has more. Condition: his heuristic, not a measured limit. [658d97cafe81]
5. **Copy sequence: call out the problem, back it with punchy information, tie in the product as the solution, stack as many benefits as possible.** Bite example benefits: "healthier teeth, cleaner planet", "put your care on autopilot", with checkmarks. [658d97cafe81]
6. **Everything needed to decide goes above the fold, with the button right there ("button at the top").** Logo, headline, short copy and a button sit at the top. Reason: many people do not scroll, and with no button above the fold a non-scroller has "zero chance" to click. In the Bite email the button comes after "two quick sentences". The top section is an "elevator pitch". Condition: the presenter's reasoning. The transcript does not say "mobile"; mobile is header only and card inference. [9a3babffe41e] [c69f1a6ad23e]
7. **Bigger buttons get more clicks.** Transcript: "The bigger the [button], the more clicks" (the transcript says "email"; context is the button). He says he would make Dr. Squatch's hero button "a lot bigger" and praises a "massive" hero button in the "Grunes" email. Condition: opinion backed by examples, not tests. [9a3babffe41e] [ad381d809315]
8. **Put a button at the end of every section.** Reason: a reader who stops after a section and finds no button just leaves. Buttons in the "find your flow" example sit close together. Condition: the card warns too many buttons can dilute a single goal; that caveat is the card writer's. [c69f1a6ad23e]
9. **The middle is a "bridge" that justifies the top claim with infographics, not paragraphs.** Use icons, larger highlighted ingredient names, a headline that summarises the section, and a short line of detail for those who want it. [c69f1a6ad23e] [658d97cafe81]
10. **Make the scroll feel seamless.** Use background gradients and one flowing background so the reader does not notice they are scrolling. The "find your flow" email goes blue to purple to a final background image. A "blocky" email (Dr. Squatch product section) makes people "more likely to fall off after they reach the end of the section". Condition: his reasoning, no scroll-depth data. [b974561edcc8]
11. **Good design keeps people subscribed, even when a single email does not sell.** "Fun, immersive designs may not convert today", but keep people engaged and coming back. Good design lowers unsubscribes and builds positive associations (his claim, no numbers). Aim for both conversion and looks. [9fe5472706f8] [ad381d809315]
12. **Elevate the basics. Do not explode the email with colour.** Design takeaways from the "Grunes" email: big buttons, matched colours and accent colours throughout, infographics, and care with small details. [ad381d809315]
13. **Image-only emails are fine (presenter's position).** "It is 2026. You do not need to be worried about having text and HTML in your emails." Evidence: all the "7 to 9 figure brands" he has worked with do it (transcript says "over 27 to9 figure brands", likely "20" plus "7 to 9 figure"; the card reads it as 20-plus), and 1 "$200 million a year brand" sends only image slices. Condition: contested; see section 9. [cfa416cb8d27]
14. **Copy other brands that do email well.** His "favorite thing" in copywriting is to copy strong brands like Bite, then rebuild with ChatGPT (procedure 3.1). Condition: copy the structure. The card adds that verbatim copying is not endorsed and has legal risk. [fab16f82f356]

## 3. Procedures

### 3.1 Reverse-engineer a competitor email into a copy template with ChatGPT

1. Pick an email you think is well written (he used a Bite email). [fab16f82f356]
2. Give it to ChatGPT and prompt: "Please transcribe this email copy."
3. Prompt: "Can you please analyze the copy and create a reusable template?"
4. Give your brand details ("Here's my brand").
5. Prompt: "Please write this email for me following the exact formula you gave."
6. Answer its questions. It asked for the angle; he gave "if your soap is white and perfect looking, it's probably fake". It asked for positioning; he gave "the ancient craft".
7. Output example (soap brand): headline "Is your soap too perfect to be real?", opener "If your bar is neon white, has sharp edges, and smells like tropical breeze, [it] was built in a lab, not made by human hands", CTA "Upgrade to real soap", then sections "The pretty soap lie", "The truth they don't tell you", "What real soap looks like", closing CTA "Choose the real soap".
8. Edit before use. He says it took about 2 minutes and he would "adjust some things".
9. Card addition (not in transcript): keep the template on file for future angles; verify claims and regulated wording. [fab16f82f356]

### 3.2 Map the email layout in Figma `[verify UI]`

1. Open Figma. Create a file, choose "Design". Name the file. [e34234698845]
2. Always build inside a frame. Draw a frame 600 wide. Height is set by content (his ButcherBox email ran long because of copy).
3. Pick a reference email for the layout (he copied the "Grunes" layout).
4. Drop labelled text boxes as placeholders, in order: logo, headline (size about 30), body copy (smaller for an educational email), CTA, graphic, sub-headline, body copy, us-versus-them infographic, CTA, footer.
5. Use the map to get unstuck: "If you ever get stuck with designing, just start off with mapping things out."
6. You can ignore advanced panels (layout, stroke, effects) when starting.

### 3.3 Add brand, copy and buttons in Figma `[verify UI]`

1. Import the logo image. Drag it into the frame; Figma shows centring guides. The layers panel on the left groups items inside the frame. [e34234698845]
2. Paste finished copy from your doc (he wrote copy in a Google Doc; the walkthrough skips copywriting). Separate text boxes or 1 box both work.
3. Set the brand font (ButcherBox: Montserrat). He tried bold, found it "a little bit bold", and used semibold.
4. Build a button: draw a rectangle over the CTA text, select both, group them, optionally name the group "button one", and keep the text above the rectangle. Centre it.
5. Set button colour from the brand site (ButcherBox uses red for CTAs), text white.

### 3.4 Set colours and a seamless background in Figma `[verify UI]`

1. Choose the hero graphic before setting colours. "That's going to determine like the coloring that I use throughout this email." [e34234698845] [b974561edcc8]
2. Drop the image in, right-click, send it to the back.
3. Draw a rectangle as the background, send it to the back, and use the colour picker (eyedropper) to sample the image's background colour.
4. If shades still differ at a seam, draw another rectangle, set a gradient fill from the top colour to the colour it fails to blend with, and position it over the seam. Adjust gradient stops so it settles into a solid colour. Holding Command while resizing helped him fit it.
5. For the lower sections, set the frame fill itself to the same beige/orange colour so the background is continuous. Keep text layers above the gradient.
6. Add accent colour in small places. He added red to a discount-code bar with the button and a "last chance" label, copying how the "Grunes" email repeats yellow accents. [b974561edcc8] [ad381d809315]

### 3.5 Build an us-versus-them block in Figma `[verify UI]`

1. Write a sub-headline that states the single strongest claim. Example: "Not all human grade dog food is created equal." Body: "Human grade sounds premium but it still allows factory farmed meat, antibiotics, and nutrient killing heat. We don't cut corners. We raise the bar. Give your dog more than a claim. Give them food with integrity." [179e3a5ac735]
2. Put the brand (logo, "us") on the left and competitors on the right (label "Them" / "most human grade brands").
3. List your points as text boxes. Copy the column for competitor points.
4. Bold your points only. Leave competitor points unbolded.
5. Add a check icon to each of your points and an X to each competitor point. He gets free icons from the Noun Project.
6. If it looks flat, put each column in a box: rounded corners via corner radius (he used 20), add a stroke and thicken it. He used grey for one box and white for the other so one stands out (the card says white for the brand column; the transcript does not say which side is white).
7. Repeat the CTA button right after the block. He considered a second CTA above it and dropped it.

### 3.6 Finish the email and footer in Figma

1. Add a product picture if you have one, for colour and life (he had few brand assets). [ad381d809315]
2. Footer: lead with the main CTA (for ButcherBox for Pets, the quiz that builds a dog's custom plan, used in the footer of all their emails), buttons to shop other options, a website link, and social icons. [5b334bf3aab6]
3. If the footer floats, add a background shape in the accent colours. He also added a fun dog image found online (check image rights; the source does not).
4. Final checklist he reads back: pain or benefit headline, short copy used sparingly, big button at the top, graphic, 1 colour flowing throughout, 1 accent colour (red) carried through, us-versus-them infographic with bold main points, final CTA, footer with buttons.

### 3.7 Slice and export from Figma `[verify UI]`

1. Do not export the whole email as 1 image. It is a huge file and may load slowly in the inbox. [8ae50e9df495] [2dabf0e92513]
2. Use the Slice tool to draw slices. He gives no pixel height; he shows a section-sized slice as the maximum ("at most... kind of like this size").
3. Export at 2x. Name files in order (1 YouTube, 2 YouTube...).
4. Slice by link: an image can carry only 1 link. Make the footer logo its own slice, split the social icons and footer buttons into separate slices, and use a table (columns) in the ESP to place side-by-side slices.

### 3.8 Compress images

1. Go to iLoveIMG (iloveimg.com, compress image). Upload all slices, click Compress, download. [2dabf0e92513]
2. His set dropped from 4.4 MB to 1.26 MB, 72% smaller (example, not a target).
3. Card addition: check quality after compressing.

### 3.9 Upload and send in Omnisend `[verify UI]`

1. Campaigns, create campaign, choose Email. [400d584b7e15]
2. Enter subject line, sender name and preheader (preview text). Example: subject "Last chance for 20% off", preheader "Open for your last gift opportunity".
3. Pick any template to get a canvas, then delete all its content.
4. Add image elements (drag and drop, duplicate for speed) and upload the compressed slices in order.
5. Select the images and remove image padding. Also remove the side padding in the containing frame (he notes you need to "click around" to find it). Resize to full width.
6. Paste 1 destination link per image.
7. Add alt text per image (e.g., "Your dog's custom plan expires tonight", "picture of dog food"). He calls it optional: it "helps a little bit with deliverability, but honestly, I haven't really seen an impact".
8. Preview. Omnisend warned "Your email lacks an unsubscribe link" and added one for compliance.
9. Send a test email to yourself to double-check everything.
10. Save, choose recipients: all subscribers, a segment, or exclude a segment. Review and send.
11. The same flow applies to a flow email (he mentions flows but demos a campaign). Klaviyo is named in the header and cards only. [verify UI] for any other ESP.

### 3.10 Hidden text block (header only, not in transcript)

The curator's header describes it: paste the brand's "About Us" copy at the bottom of an image-heavy email, set it to size 5 with 5% line spacing, colour matched to the background, to pass spam filters that penalise low text-to-image ratio. The card adds: place after footer, use real brand copy, preview for extra scroll space. Do not run this without review; see section 9. [9efe76ee1d22] `[web check: current Gmail and ESP policy on hidden or invisible text and text-to-image ratio]`

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Email frame width | 600 (px) | Figma frame start size | "I always like to do dimensions of 600 width" | [e34234698845] [8ae50e9df495] |
| Headline size in layout map | about 30 | placeholder stage | walkthrough | [e34234698845] |
| Body copy before the top button | about 2 short sentences | hero section | Bite example | [9a3babffe41e] |
| Biggest body block | 1 sentence | promo email | Bite example | [658d97cafe81] |
| Selling points | 3 | per email argument | "brain can only take three things" (heuristic) | [658d97cafe81] |
| Attention span | 3 seconds | header only | curator's summary | [658d97cafe81] |
| CTA buttons | 1 at the top plus 1 at the end of each section | all promo layouts | reasoning | [c69f1a6ad23e] |
| Button size | "bigger the better" | all buttons | opinion | [ad381d809315] |
| Corner radius on comparison boxes | 20 | us-versus-them block | walkthrough | [179e3a5ac735] |
| Export scale | 2x | Figma slices | walkthrough | [8ae50e9df495] |
| Links per image | 1 | every slice | platform behaviour | [8ae50e9df495] |
| Compression result | 4.4 MB to 1.26 MB, 72% | one example set | walkthrough | [2dabf0e92513] |
| Slice height | no number given | "at most" section size | not stated | [2dabf0e92513] |
| Hidden text | font size 5, 5% line spacing, colour = background | header only | curator's summary | [9efe76ee1d22] |
| Offer in demo | 20% off, expires tonight | ButcherBox for Pets example | example copy | [400d584b7e15] |

The source gives no image-to-text ratio number, no file-size limit, no font-size minimum for body text and no spacing values.

## 5. Diagnostics and checks

- **Where does the email fail?** Card method (card writer's split, not the presenter's): readers do not reach the offer, fix structure and button placement first; they reach it but do not click, test copy clarity and offer framing; it feels cheap or off-brand, fix design. [9fe5472706f8] `[needs brand data: click maps or click-by-link report, scroll or open-to-click by email]`
- **Is there a button above the fold?** Open the preview. Good: logo, headline, 1 to 2 sentences and a large button visible without scrolling. Bad: button after a graphic or far down. Fix: move the button directly under the hero copy. The fold varies by device and ESP; check in preview. [9a3babffe41e]
- **Does every section end with a button?** Good: yes. Bad: a section ends with no click target. [c69f1a6ad23e]
- **Is any block a paragraph?** Bad: "big paragraph with a whole bunch of jargon". Fix: checklist, icons, highlighted key words, comparison graph. [658d97cafe81]
- **Is it blocky?** Scroll top to bottom. Bad: visible colour seams or alternating hard-edged blocks. Fix: shared background colour, gradient rectangle over the seam. [b974561edcc8]
- **Are accent colours repeated?** Good: 1 accent (e.g., CTA red) on button, discount bar and urgency label. [ad381d809315]
- **Is each link on its own slice?** Check each footer icon and button goes to its own URL. [8ae50e9df495] [5b334bf3aab6]
- **Are slices compressed and seamless?** Check file sizes dropped, no quality loss, no padding gaps in the ESP. [2dabf0e92513] [400d584b7e15]
- **Pre-send:** unsubscribe link present, alt text on each image, test email to self, correct segment and exclusions. [400d584b7e15]

## 6. Tools, settings and named features

- **Figma** `[verify UI]`: Design file, Frame (600 wide), text boxes, font panel, Rectangle, Group, layer naming, right-click send to back, colour picker/eyedropper, gradient fill with movable stops, corner radius, stroke, Slice tool, export at 2x. He calls it "the best design app". [e34234698845] [8ae50e9df495]
- **ChatGPT**: transcribe, template, rewrite prompts (3.1). [fab16f82f356]
- **Noun Project**: free check and X icons. [179e3a5ac735]
- **iLoveIMG** compress image: bulk compress slices. [2dabf0e92513]
- **Omnisend** `[verify UI]`: campaigns, email editor, template canvas, image elements, image padding, frame padding, tables for side-by-side slices, links, alt text, auto unsubscribe link warning, preview, test send, recipients and segment exclusions. Affiliate link given (30% off). [400d584b7e15]
- **Klaviyo**: named in header and cards only, not demonstrated. `[verify UI]`
- **Google Docs**: where copy is written before paste.

## 7. Examples and case results

All are examples, not promises. None has performance numbers.

- **Bite (toothpaste):** pain headline, 2 sentences, button, 1-sentence body block, 3 ingredients, checkmarked benefits. Second Bite email: "Is your phone lying to you?" [658d97cafe81]
- **"Find your flow" email (brand unnamed):** logo, headline, copy and button at top; icon infographic bridge; button at the end of every section; blue to purple to image background gradient. [c69f1a6ad23e] [b974561edcc8]
- **Dr. Squatch:** right structure, but hero button too small and a "blocky" product section. [9a3babffe41e]
- **"Grunes"/"Grooms" (gummies):** massive hero button with border and shadow for a 3D look, yellow border on the image, varied text weight, repeated green, lined-text callout, graph comparing tablets vs gummies, lifestyle images, big buttons throughout. The card calls this Gymshark; the transcript does not support that, and gummies vs tablets fits a supplement brand. [ad381d809315]
- **ButcherBox for Pets build:** headline "Your dog's custom plan expires tonight"; body on the custom plan and a 20% off offer expiring; red CTA; beige background from the product image; red discount bar and "last chance" label; us-versus-them block; quiz CTA in the footer. [e34234698845] [179e3a5ac735] [5b334bf3aab6]
- **Soap brand (ChatGPT output):** see 3.1. [fab16f82f356]
- **"$200 million a year brand":** sends image-only emails. Presenter claim. [cfa416cb8d27]
- **Compression:** 4.4 MB to 1.26 MB (72%). [2dabf0e92513]
- **Presenter claims:** $150M email revenue in 4 years; 200 brands; $500,000 per month for 1 brand. Marketing claims, not benchmarks. [9fe5472706f8]

## 8. Mistakes the source warns about

1. Caring more about how the email looks than how it performs. [9fe5472706f8]
2. Placing the first button far down, so non-scrollers cannot click. [9a3babffe41e]
3. Small hero buttons (Dr. Squatch). [9a3babffe41e]
4. Sections that end with no button. [c69f1a6ad23e]
5. Big paragraphs of jargon instead of infographics. [c69f1a6ad23e] [658d97cafe81]
6. Blocky sections that break the scroll. [b974561edcc8]
7. Boring or ugly design; also the opposite, "crazy colors and all this fancy stuff". [ad381d809315]
8. Exporting the whole email as 1 image (slow load, only 1 link). [2dabf0e92513] [8ae50e9df495]
9. Putting several click targets on 1 slice (e.g., whole footer linking to the quiz only). [8ae50e9df495]
10. Uploading uncompressed slices. [2dabf0e92513]
11. Leaving default image and frame padding, which shows gaps. [400d584b7e15]
12. Worrying that image-only emails are a problem (his view; contested). [cfa416cb8d27]

## 9. Caveats, conflicts and what is missing

- **Image-only emails conflict with common deliverability and accessibility advice.** Screen readers and image-blocked inboxes get only alt text. Text is not searchable or selectable. The card suggests adding a plain-text or HTML text version where the ESP supports it; the presenter does not say this. `[web check: current Gmail, Yahoo and Apple Mail image blocking and accessibility guidance]` `[needs brand data: share of opens with images off, deliverability history for image-only vs HTML sends]` [cfa416cb8d27]
- **Hidden text hack is header only and risky.** The transcript never covers it. Invisible text is a known spam signal and may break ESP or mailbox terms. Do not use it by default. [9efe76ee1d22] `[web check: Gmail and ESP policy on hidden text]`
- **Header and cards add details the transcript lacks:** "mobile" fold, "3-second" attention span, footer "Men/Women" category buttons, Gymshark, Klaviyo. Treat them as curator or card-writer additions. [9a3babffe41e] [c69f1a6ad23e] [ad381d809315]
- **No data behind any rule.** Bigger buttons, repeated buttons, gradients and footer navigation are opinion and screenshots. `[needs brand data: A/B tests on button size, button count and layout; click-by-position reports]`
- **Missing how:** no slice height or file-size limit, no body font size, no spacing or margin values, no dark-mode check, no mobile-specific layout advice, no image-to-text ratio number, no subject line or preheader method beyond 1 example, no rules on how many products to feature.
- **Competitor copying:** copy the structure and angle only. Comparative claims about competitors need substantiation. `[needs brand data: substantiation for each us-versus-them claim]` [179e3a5ac735] [fab16f82f356]
- **Urgency copy:** "expires tonight" and "last chance" must be true for the brand's offer. `[needs brand data: real offer end time]`
- **Image rights:** he used a dog image "off the internet". Use owned or licensed images; use real product photos where accuracy matters.
- **Omnisend affiliate:** the ESP choice is sponsored; the method works in other ESPs but menus differ. `[verify UI]`
- **Brand inputs needed to run this:** `[needs brand data: brand fonts, CTA colour, logo, hero and product images, 3 main selling points, top categories for footer links, quiz or main landing URL, current offer]`

## 10. Card index

- [9fe5472706f8] Three components of a converting email: copy, structure, design
- [9a3babffe41e] 'Button at the top' rule for non-scrollers
- [c69f1a6ad23e] Email structure: hero, bridge, repeated CTAs, footer navigation
- [b974561edcc8] Make the email scroll feel seamless with gradients and flowing backgrounds
- [658d97cafe81] Skimmable copy: pain headline, one-sentence body, three selling points
- [fab16f82f356] Reverse-engineer competitor emails into a reusable copy template with ChatGPT
- [8ae50e9df495] Build emails as stacked image slices, not one giant image
- [9efe76ee1d22] Hidden footer text to protect text-to-image deliverability ratio
- [e34234698845] Laying out an email design in Figma without advanced tools
- [179e3a5ac735] Us-versus-them comparison block built with icon checkmarks
- [5b334bf3aab6] Put footer navigation to work for non-buyers
- [400d584b7e15] Upload a finished image-design email into an ESP as stacked images
- [cfa416cb8d27] Image-only vs text-and-HTML emails: the presenter's position
- [2dabf0e92513] Compress and slice images to protect load time in the inbox
- [ad381d809315] Design principles that keep emails converting and subscribers subscribed
