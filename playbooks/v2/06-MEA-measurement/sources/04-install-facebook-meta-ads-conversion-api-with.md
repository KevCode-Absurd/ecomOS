# Install Facebook (Meta Ads) Conversion API with server-side tagging

source_id: 1hqJghZ6POtNwWAMCKIdbJqUS7O7Y8lPK  |  folder: /06-MEA-measurement  |  cards: 7  |  words: 5,023  |  type: transcript (YouTube tutorial, screen-share walkthrough)

credibility: Presenter is Leon, who runs a YouTube channel "to help you make better decisions in your daily work using your web stats". He sells nothing directly in the video but promotes a Stape affiliate link (Stape is a server-side GTM host), a free mini-course on server-side tracking with Stape given through that link, and a free "grow your website traffic" cheat sheet. The Conversions API template he uses is made by Stape, so there is a commercial tie to the tool choice. Evidence is 1 live demo on his own site (PageView and a contact form), shown in GTM preview and Meta Events Manager. No client data, no before-and-after numbers, no match quality or attribution results. He says the redundant setup "is how meta ads recommends", without citing Meta.
date signals: No year given. Events Manager labels the pixel ID as "dataset ID", which dates it after Meta renamed pixels to datasets. Uses GA4 and Google Consent Mode (ad_storage). Builds on the presenter's earlier videos on server-side GTM, GA4 and consent mode. File in export is titled "...with server-side GTM"; the Drive title says "server-side tagging". Drive modified date 2026-09-20 is the file date, not the recording date. The source's triage header files it under 11-ADC (tracking pixels, deduplication); it now lives in 06-MEA. All UI steps are a snapshot `[verify UI]`.

## 1. What this source is for

It shows how to send Meta events 2 ways at once: the browser pixel from a normal (web) GTM container and the Conversions API (CAPI) from a server-side GTM container. It then merges the 2 copies with a shared Event ID so each event counts once. It adds 2 safety steps: consent gating on both sides, and a test event code that only turns on in GTM preview. Use it as the build and QA checklist for a GTM-based Meta CAPI setup. It only covers PageView and a Contact (form) event. It does not cover Purchase, value, customer data parameters or event match quality.

## 2. Principles

1. **Run a redundant setup: same event from browser and server.** Keep the Meta pixel firing client-side in the web GTM container, and send the same events to CAPI from the server GTM container. In Events Manager each event then shows once from "browser" and once from "server". Condition: presenter says this is Meta's recommended setup; he shows it working for PageView and Contact. Evidence: live demo only. [0b762a508449]
2. **Redundancy and deduplication must ship together.** Without deduplication, Meta counts every event twice. Dedup works by sending the exact same Event ID in both streams. Condition: always, for any event sent both ways. [0b762a508449] [0954c80debf4]
3. **Server events arrive later than browser events.** In the demo the server Contact event showed up a short while after the browser one. Condition: wait before calling the server tag broken. No delay figure given. [0b762a508449] [8d023b8f223e]
4. **Do not send anything to Meta without consent.** Presenter stresses this several times. Client tag requires ad_storage consent. Server triggers require the consent-mode variable to show granted. Condition: sites with a cookie banner and consent mode. He does not discuss regions where consent is not required. [1cdafb95b157] [44e509c9fd36]
5. **Fire the consented pixel on the page where the user opts in.** Using the Initialization - All Pages trigger means the pixel is blocked on the first page and only fires on the next page. Trigger on the cookie consent update event instead. Condition: consent-gated pixel with a banner. Evidence: demo in GTM preview. [1cdafb95b157]
6. **Prefer explicit control over inheritance on the server tag.** "Inherit from client" is fine for default events, but the presenter sets Event Name Setup Method to Override so he names each event sent. Presenter preference. [44e509c9fd36]
7. **Store IDs and tokens once, in constant variables.** Pixel ID and token go into GTM constant variables, not pasted into each tag. Variables are not shared between the web and server containers, so each container needs its own copy. [729a4812f715] [44e509c9fd36]
8. **Never let a test event code reach production.** A test ID left in a published tag sends real users' events to the Test Events screen, where they do not count. Presenter says he has done this "so many times" and "missed a lot of data". Fix: a lookup table on Debug Mode so the test ID exists only in preview. [e1c161b2fe2d]
9. **The real dedup proof is a matching ID, not a green tag.** The server tag forwards the Event ID automatically, but the presenter says "sometimes this doesn't work". The final check is to find the same Event ID on the browser and server copies. [0954c80debf4] [8d023b8f223e]

## 3. Procedures

### 3.0 Preconditions (from the presenter's earlier videos, not shown here)
1. A web (client-side) GTM container on the site.
2. A server-side GTM container, set up and receiving hits. Presenter hosts with Stape (affiliate). `[web check: server GTM hosting options and cost]`
3. GA4 installed in both containers. The GA4 events from the web container are what trigger the server-side Meta tags.
4. Consent Mode set up, with a cookie consent update dataLayer event and a consent-mode variable readable in the server container. The source does not show how to build these. [0b762a508449] [1cdafb95b157]
5. A form that fires a `contact form submit` event and redirects to a thank-you page (demo site). Swap in the store's own conversion events. `[needs brand data: list of the store's conversion events and their dataLayer names]` [8d023b8f223e]

### 3.1 Get the 2 credentials `[verify UI]`
1. Open Meta Events Manager > Data sources. Select the pixel. [729a4812f715]
2. Copy the pixel ID. In the presenter's UI it is labelled "Dataset ID". Save it (he uses a text file named "meta ads pixel ID"). [729a4812f715]
3. Still in Data sources, open Settings. Scroll to the "Conversions API" section. Click "Generate access token". Copy and save the token ("meta ads token"). [729a4812f715]
4. If the Generate button is greyed out, you lack permission. Ask the account admin to generate it and send it to you. [729a4812f715]
5. Treat the token as a secret. (The source stores it in a text file and a GTM constant; it gives no security advice. For ecomOS, keep tokens out of shared docs and chat.)

### 3.2 Step 1: client-side pixel in the web GTM container `[verify UI]`
1. Variables > New > Constant. Name "Meta Ads Pixel ID". Value: the pixel ID. Save. [729a4812f715]
2. Tags > New. Name used: "02 Meta Ads - Page View" (presenter numbers tags). [1cdafb95b157]
3. Tag configuration > Community Template Gallery > search "Facebook" > pick the "Facebook Pixel" template by "facebookarchive" > Add to workspace. [1cdafb95b157]
4. Facebook Pixel ID field: `{{Meta Ads Pixel ID}}`. [729a4812f715]
5. Event name: standard `PageView`. [1cdafb95b157]
6. Advanced Settings > Consent Settings > "Require additional consent for tag to fire" > add `ad_storage`. [1cdafb95b157]
7. Trigger: first set to Initialization - All Pages (to show the problem), then change to the cookie consent update event (see 3.3). Save. [1cdafb95b157]
8. The source later refers to a client-side Contact pixel tag (it adds the Event ID to it in 3.7) but does not show building it. Build it the same way with the Contact event and the form trigger. The source is thin here.

### 3.3 Test and fix the consent trigger (GTM preview) `[verify UI]`
1. Preview > connect to the site. Banner is showing; no consent yet. [1cdafb95b157]
2. Tag Assistant > Summary: the Meta tag has not fired. Under the Initialization event it shows "blocked by consent settings". Good: nothing sent before consent. [1cdafb95b157]
3. Click "Allow all". With the Initialization trigger the tag still does not fire on this first page. It fires only on the next page. Bad: the first page view after opt-in is lost. [1cdafb95b157]
4. Fix: change the tag's trigger from Initialization - All Pages to the cookie consent update dataLayer event. Save. [1cdafb95b157]
5. Reset consent: browser Inspect > Application > Cookies > delete the consent cookie. Refresh preview. [1cdafb95b157]
6. Retest: before consent the tag does not fire. After "Allow all" it fires on the same first page. [1cdafb95b157]

### 3.4 Step 2: server-side CAPI tags in the server GTM container `[verify UI]`
1. Tags > New. Name used: "02.01 Meta Ads - Page View". [44e509c9fd36]
2. Tag configuration > Community Template Gallery > search "Facebook" > pick "Facebook Conversions API" template by Stape > Add to workspace. [44e509c9fd36]
3. Event Name Setup Method: Override (Inherit from client is allowed for default events). Select `PageView`. [44e509c9fd36]
4. Action Source: Website (default left as is). [44e509c9fd36]
5. API Access Token: new Constant variable "Meta Ads Token" with the token. [44e509c9fd36]
6. Facebook Pixel ID: new Constant variable "Meta Ads Pixel ID" in this container (it does not carry over from the web container). [44e509c9fd36] [729a4812f715]
7. Trigger: new trigger "All Pages with consent". Type Page View > Some Page Views > condition on the consent-mode variable showing consent granted. Presenter built that variable in his consent-mode video. [44e509c9fd36]
8. Save. [44e509c9fd36]

### 3.5 Server-side conversion tag (Contact example) `[verify UI]`
1. Tags > New. Name used: "02.02 Meta Ads - Contact". Same Stape Conversions API template. [44e509c9fd36]
2. Override event name > `Contact`. Token: `{{Meta Ads Token}}`. Pixel ID: `{{Meta Ads Pixel ID}}`. [44e509c9fd36]
3. Find the incoming event name: turn on preview in both containers, submit the form (presenter types "test"), land on the thank-you page. In the server preview a `contact form submit` event arrives. In the demo it only appeared after refreshing the thank-you page. [44e509c9fd36]
4. Triggering > new trigger. Type Custom Event. Event name must exactly match the name seen in server preview (`contact form submit` as spoken). Put the event name in the trigger title for clarity ("Contact form submit with consent"). [44e509c9fd36]
5. Add condition: consent-mode ad_storage variable contains "granted". Save trigger and tag. [44e509c9fd36]
6. For a store, repeat for each conversion event with the matching Meta standard event. The source does not show Purchase or AddToCart. `[needs brand data: event map from store events to Meta standard events]`

### 3.6 Test event code with a Debug Mode lookup table `[verify UI]`
1. Events Manager > Data sources > Test events tab. Copy the test event code shown. [e1c161b2fe2d]
2. Naive way: paste the code into the Test ID field of the server Meta tag. Risk: publishing with it left in (see section 8). [e1c161b2fe2d]
3. Better way: Variables > New. Name "Meta Ads Test ID". Type Lookup Table (not Constant). [e1c161b2fe2d]
4. Input variable: Debug Mode (a built-in variable; enable it under built-in variables if not listed). [e1c161b2fe2d]
5. Default value: leave empty. So a normal visit sends no test ID. [e1c161b2fe2d]
6. Add 1 row: input `true` > output = the test event code. Debug Mode is true only while GTM preview is open. [e1c161b2fe2d]
7. Put `{{Meta Ads Test ID}}` in the Test ID field of every Meta server tag (presenter: Page View and Contact). Save. [e1c161b2fe2d]
8. Before each new test session, check the code in Test events. It can change between days; if so, update the row output by hand. [e1c161b2fe2d]

### 3.7 Test both streams before dedup `[verify UI]`
1. Preview the server container. Open the homepage with the web preview on. [8d023b8f223e]
2. Web side: Meta Ads Page View tag fired. [8d023b8f223e]
3. Server side: a page view event arrives, and the Meta Ads Page View tag shows "succeeded". If it shows failed, re-check the token and pixel ID values. [0b762a508449] [8d023b8f223e]
4. Events Manager > Test events: 2 PageView events, 1 "browser" and 1 "server". [8d023b8f223e]
5. Submit the form again. Server preview shows `contact form submit` and Meta Ads Contact "succeeded". Events Manager shows 1 browser and 1 server Contact. [8d023b8f223e]
6. At this point every event is counted twice. Do not publish without step 3.8. [0954c80debf4]

### 3.8 Step 3: deduplicate with a shared Event ID `[verify UI]`
1. Web container > Variables > New. Name "Event ID". Community Template Gallery > search "event ID". Presenter uses the template by Markus Baersch ("m barsh" in transcript); he says the stape.io one is "also very good". Add to workspace. [0954c80debf4]
2. The gallery dialog had a small bug in the demo; close it and create the variable again. The template needs no settings. Save. [0954c80debf4]
3. Client pixel tags: open Meta Ads Page View > More Settings > Event ID = `{{Event ID}}`. Repeat for the Contact pixel tag and any other pixel tag. Save. [0954c80debf4]
4. Server side: send the same ID through the GA4 events, because they trigger the server Meta tags. Open the GA4 page view tag > Event Parameters > add parameter named "event ID" (as spoken) with value `{{Event ID}}`. Save. `[web check: exact parameter key the Stape Meta CAPI tag reads, often written event_id]` [0954c80debf4]
5. Do the same on the GA4 contact form submit event tag, and on every GA4 tag that drives a Meta server event. [0954c80debf4]
6. The Stape Meta tag reads that key from the event data and forwards it in the outgoing CAPI request automatically. No field to set on the server tag in the demo. [0954c80debf4]
7. Preview again. In server preview open the GA4 page view > Event Data: `event ID` is present. Open the Meta tag's outgoing request: the event ID is in it. [0954c80debf4]
8. Events Manager > Test events: the new PageView shows the server event as deduplicated. [0954c80debf4]
9. Final proof: copy the Event ID from the browser event, then Ctrl+F (Cmd+F on Mac) in Events Manager. Both the browser and server event must carry the same ID. [0954c80debf4] [8d023b8f223e]
10. Repeat 9 for the Contact event. Then publish both containers. The test ID drops out by itself because Debug Mode is false for real visitors. [e1c161b2fe2d]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Credentials needed | 2: pixel (dataset) ID + CAPI access token | any CAPI setup | demo | 729a4812f715 |
| Streams per event | 2: browser + server, then merged to 1 | redundant setup | "how Meta recommends", no citation | 0b762a508449 |
| Dedup key | identical Event ID in both streams | every event sent both ways | demo | 0954c80debf4 |
| Client consent | require `ad_storage` | sites with consent mode | demo | 1cdafb95b157 |
| Client trigger | cookie consent update, not Initialization - All Pages | consent-gated pixel | demo: Initialization loses the opt-in page | 1cdafb95b157 |
| Server consent | consent-mode ad_storage "contains granted" on every trigger | all server Meta tags | presenter stress | 44e509c9fd36 |
| Server event name | Override, not inherit | presenter preference; inherit OK for default events | opinion | 44e509c9fd36 |
| Action source | Website | web events | demo | 44e509c9fd36 |
| Custom event trigger name | exact match to incoming event name | server triggers | demo | 44e509c9fd36 |
| Test ID default | empty | lookup table on Debug Mode | demo | e1c161b2fe2d |
| Test ID on | only when Debug Mode = true | preview sessions | demo | e1c161b2fe2d |
| Test code freshness | may change day to day | before each test session | presenter note | e1c161b2fe2d |
| Server event timing | arrives after browser event | when checking Events Manager | demo; no delay number | 0b762a508449 |

The source gives no numeric thresholds (no match quality score, no dedup rate, no delay window, no volume).

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Pixel blocked before consent | GTM preview, banner not answered | Meta tag "blocked by consent settings" | Tag fired | Add ad_storage consent requirement | 1cdafb95b157 |
| Pixel fires on opt-in page | Delete consent cookie, preview, click Allow all | Tag fires on the same first page | Fires only on page 2 | Switch trigger to cookie consent update | 1cdafb95b157 |
| Server receives event | Server container preview | page view / conversion event listed | Nothing arrives | Check web-to-server GA4 setup (earlier videos); for thank-you pages, refresh | 44e509c9fd36 8d023b8f223e |
| Server Meta tag status | Server preview > tag | "succeeded" | failed / false | Re-check token and pixel ID values | 0b762a508449 8d023b8f223e |
| Both streams land | Events Manager > Test events | 1 browser + 1 server per event | Only browser | Wait (server lags), then re-check trigger name match and consent condition | 8d023b8f223e |
| Event ID on GA4 event | Server preview > Event Data | `event ID` present | Missing | Add event parameter on every GA4 tag that drives Meta | 0954c80debf4 |
| Event ID forwarded | Server preview > Meta tag outgoing request | event ID in request | Missing | Check parameter key name `[web check: key the tag reads]` | 0954c80debf4 |
| Dedup works | Copy browser Event ID, Ctrl/Cmd+F in Test events | same ID on browser and server copy; server marked deduplicated | Different or missing IDs | Fix Event ID wiring; re-test; do not trust counts until fixed | 0954c80debf4 8d023b8f223e |
| Test ID off in production | Normal (non-preview) visit, inspect request or Events Manager | No test ID; events in live data | Live events land in Test events | Replace hard-coded Test ID with the lookup table variable | e1c161b2fe2d |
| Test ID current | Events Manager > Test events before testing | Code matches lookup row | Code changed | Update lookup output | e1c161b2fe2d |

Not covered by the source, needed for a full audit: event match quality score per event, customer information parameters, deduplication rate shown in Events Manager, Purchase value and currency accuracy vs store orders. `[web check: where Events Manager shows event match quality and dedup status today]` `[needs brand data: Meta Purchase count and value vs store order data for the same days]`

## 6. Tools, settings and named features

- **Meta Events Manager** `[verify UI]`: Data sources > Dataset ID (pixel ID); Settings > Conversions API > Generate access token; Test events tab (test event code; test events do not count in real data). [729a4812f715] [e1c161b2fe2d]
- **Google Tag Manager, web container**: Community Template Gallery; "Facebook Pixel" template by facebookarchive (fields: Pixel ID, Event name, More Settings > Event ID); Advanced Settings > Consent Settings > Require additional consent (ad_storage); Tag Assistant preview. `[verify UI]` [1cdafb95b157] [0954c80debf4]
- **Google Tag Manager, server container**: "Facebook Conversions API" template by Stape (fields: Event Name Setup Method inherit/override, Action Source, API Access Token, Facebook Pixel ID, Test ID); Page View and Custom Event triggers; built-in Debug Mode variable; Lookup Table variable; preview with outgoing request view. `[verify UI]` [44e509c9fd36] [e1c161b2fe2d]
- **Event ID variable template**: by Markus Baersch (presenter's choice); Stape's alternative named as good. No settings. `[web check: templates still in the gallery and maintained]` [0954c80debf4]
- **GA4 tags** in the web container: carry the Event ID to the server as an event parameter. [0954c80debf4]
- **Consent Mode**: ad_storage state; cookie consent update dataLayer event. Built in an earlier video. [1cdafb95b157]
- **Stape**: server GTM hosting, promoted with an affiliate link. [0b762a508449]
- **Browser DevTools**: Application > Cookies to clear consent for re-testing; Ctrl/Cmd+F to find an Event ID. [1cdafb95b157] [0954c80debf4]

## 7. Examples and case results

- Example (demo site, not a result): 1 PageView tracked twice in Events Manager, 1 browser and 1 server, merged as 1 event through a shared Event ID. [0b762a508449]
- Example: a contact form test ("test test test") produced a browser Contact event, then a server Contact event a little later, both with the same Event ID. [0b762a508449]
- Example: with the Initialization trigger, the consented pixel only fired on the second page; after switching to the consent update trigger it fired on the first page. [1cdafb95b157]
- No numbers on data recovered, match quality, ROAS or attribution are given.

## 8. Mistakes the source warns about

1. **Leaving the test event code in a published tag.** Live events go to the Test events screen and do not count. Presenter did this many times and lost data. Fix: Debug Mode lookup table (3.6). [e1c161b2fe2d]
2. **Stopping at "both streams fire".** Without matching Event IDs every event counts twice. [0b762a508449] [0954c80debf4]
3. **Using Initialization - All Pages for a consent-gated pixel.** The opt-in page view is lost. [1cdafb95b157]
4. **Sending data to Meta without consent.** Every server trigger needs the consent condition. [44e509c9fd36]
5. **Custom event name not matching exactly.** The server trigger never fires. [44e509c9fd36]
6. **Assuming variables carry across containers.** They do not; recreate pixel ID in the server container. [729a4812f715]
7. **Wrong or malformed access token.** Server tag shows failed. [0b762a508449]
8. **Calling the server tag broken too early.** Server events arrive later. [0b762a508449]
9. **Trusting automatic Event ID forwarding.** It "sometimes doesn't work"; verify by searching the ID. [0954c80debf4]
10. **Using a stale test code.** It can change between days. [e1c161b2fe2d]
11. **Skipping the pixel part because it already exists.** Presenter asks viewers to redo it because "the details really matter" (consent and Event ID). [1cdafb95b157]

## 9. Caveats, conflicts and what is missing

- **Only PageView and Contact.** No Purchase, AddToCart, InitiateCheckout, ViewContent. No value, currency, content IDs or order ID. For a store these are the events that matter. `[needs brand data: store platform and current Meta event setup]`
- **No event match quality.** The source never mentions EMQ, customer information parameters (email, phone, external ID, fbp, fbc, IP, user agent), hashing, or how the Stape tag fills them. It gives no EMQ check. `[web check: Meta customer information parameters, hashing rules and EMQ guidance]`
- **Dedup key is incomplete.** The source says only the Event ID must match. Meta's docs describe dedup on event name plus event ID, within a time window. The source's setup keeps names aligned (PageView/PageView, Contact/Contact) but never states it. `[web check: Meta dedup rules, required matching fields and window]`
- **Event ID parameter name.** Spoken as "event ID"; exact key not shown clearly. `[web check: key the Stape tag reads]`
- **Server hosting, custom domain and cost are skipped.** They were in earlier videos. Stape affiliate tie noted.
- **Consent model is one choice.** Presenter blocks all Meta data without ad_storage. He does not cover regions without an opt-in rule, or limited/cookieless data sending. `[needs brand data: markets served and consent rules that apply]` `[web check: current consent requirements for Meta in the brand's markets]`
- **Conflict with common ecommerce advice:** Shopify and similar stores often get CAPI from the platform's native Meta integration instead of server GTM. The source does not compare the 2 routes. Running both could double-send server events. `[web check: native Shopify Meta channel CAPI option and how it dedups with a GTM setup]` `[needs brand data: which Meta integrations are already live on the store]`
- **"Meta recommends redundant setup"** is stated without a link. It agrees with common advice, but check current Meta guidance. `[web check: Meta's current redundant setup recommendation]`
- **Card framing adds context.** Card 0b762a508449 mentions iOS and ad-blocker signal loss; the source does not.
- **Security.** Source keeps the token in a text file and a GTM constant. It gives no advice on token handling or rotation.
- **The source's triage header** routes it to 11-ADC (ad deployment); it now sits in 06-MEA. Neighbour: 24-DEP-ad-deployment for Meta account structure.

## 10. Card index

- 0b762a508449  Redundant Meta Ads tracking: browser pixel plus server Conversions API
- 729a4812f715  Get the two credentials the Conversions API setup requires
- 1cdafb95b157  Consent-gate the client-side Meta pixel so it fires on the same page as opt-in
- 44e509c9fd36  Send Meta store events server-side with the Conversions API template
- e1c161b2fe2d  Automate the Meta test event ID with a Debug Mode lookup table
- 0954c80debf4  Deduplicate Meta events by passing one Event ID into both streams
- 8d023b8f223e  Verification checks that both Meta tracking streams land and merge
