# Site Security (part 5 of 5)

source_id: 1NR2jtUMB0KkTlV_QTIGSmWVT-je-24Pt  |  folder: /23-SEC-bot-and-agent-security  |  cards (whole source): 326  |  words (whole source): 273,439  |  type: course transcript (lecture + live Q&A)

**This file covers part 5 of 5 only** (the source was split into 5 equal text parts for review; a later pass merges all 5 into one mini playbook). Part 5 is roughly the last 54,400 words of the transcript. Topics covered in this part, in order: safe-coding lessons (fail fast vs. handle expected errors, defensive coding, reduce complexity), bad API design (insecure defaults, polymorphic function signatures, Express middleware arity), Node.js Buffer uninitialized-memory disclosure (a Heartbleed-style bug, with live demo), the GitHub OAuth CSRF/HEAD-request bypass case study (with full CSRF and SameSite cookie review), DNS rebinding (mechanism, real incidents, and the Host-header defense), browser process architecture (multi-process sandboxing, Site Isolation, Spectre, CORB), JavaScript language pitfalls and linting, code-clarity advice, and open-source/browser-extension supply-chain risk. It ends with the instructor's closing list of the course's core defensive principles. Parts 1 to 4 (not covered here) hold whatever came before this material in the same transcript.

credibility: A university web-security course (Stanford-style; cross-references "CS 155" as a separate, more foundational course, and recommends CS255/CS355/CS155/CS251 as follow-ons, so this is very likely Stanford CS 253 or an equivalent web-security elective). The instructor speaks from firsthand practitioner experience: their own open-source projects (WebTorrent, the "standard" JS linter preset), a personally-introduced and later fixed DNS-rebinding bug in their own code, and live, unscripted coding demos (including visible live mistakes, corrected in real time with student help). Evidence mixes first-hand engineering experience with second-hand reporting of real, named, disclosed vulnerabilities (GitHub OAuth bypass, Blizzard Update Agent, Transmission, an npm supply-chain compromise, Mirai, Heartbleed, curl funding). It is not vendor marketing and not academic theory; it is closer to "how real production security bugs actually happened, and the lesson to take from each."

date signals: References Node.js `Buffer` before `TypedArray`/`ArrayBuffer` existed natively in JS, jQuery described as "kind of old these days," a GitHub OAuth bug fixed "2 weeks" before the lecture, a Chrome buffer-overflow research example dated 2014, Heartbleed referenced with a stated year of 2017 (this conflicts with the widely reported 2014 disclosure date - likely misspoken in the lecture; verify independently), Spectre and Site Isolation discussed as relatively recent developments, and curl's maintainer described as "recently" going full-time after ~20 years as a hobbyist. Overall the material reads as roughly late-2010s to early-2020s in currency; specific version numbers, bounty amounts and org names should be treated as dated and re-checked, not as current fact.

## 1. What this source is for

Helps a developer or technical operator (not just a security specialist) recognize and avoid the specific coding, API-design and architecture mistakes that turn ordinary web-app code into a serious vulnerability - especially CSRF, DNS rebinding against local/LAN services, memory-disclosure bugs, and open-source supply-chain compromise. For an ecommerce operation, the direct relevance is: any local admin tool, POS helper app, or third-party script an ecommerce team runs; any Node/Express-style backend; and the team's own dependency hygiene (npm packages, browser extensions used by staff).

## 2. Principles

1. **Reduce complexity; it is the primary source of security bugs.** Adding one component to a system is not "one more thing" - it is one more thing that can interact with every other component already there, so the risk grows faster than the component count. Condition: applies to any code addition, not just obviously security-sensitive code. Evidence: the GitHub OAuth bug existed specifically because GET, POST and (accidentally) HEAD were all funneled through one shared code path. [47019286e6cf][c4e441b6c91e]
2. **Explicit code beats clever code, especially in security-relevant paths.** Cleverness (one-liners, relying on implicit framework "magic," polymorphic behavior) is harder to review and easier to misuse. Condition: this is presented as a strong preference, not an absolute law - the source explicitly frames "don't be overly clever" as taste/trade-off in general code, but as close to a hard rule once security is at stake. [613fd4e14efd][dabc409377d8][708eeab33a81]
3. **Fail fast on violated assumptions; handle only genuinely expected errors gracefully.** If a code path is reached that should be structurally impossible (e.g., a third HTTP method arriving at code written for only two), crash/throw rather than silently continuing - you don't know what state was left dangling. If an error is expected as part of normal operation (e.g., a user-supplied ID not found in the database), return a normal error response and keep serving. Condition: the distinction is "did I write code to handle this case on purpose" - not merely "is this an exception." [0fd2f1e28cc1][633153c6724d][fbdd4166ffd4][76589f0257127]
4. **Code defensively: assume every input and every assumption will eventually be violated**, and verify at the top of each function rather than trusting the caller. [fbdd4166ffd4][76589f0257127]
5. **APIs should be secure by default.** If safe use requires the caller to pass extra options, most callers won't, and will run insecurely. Condition: applies to any function/library your own team writes or wraps, and to third-party APIs you evaluate before adopting. [0021606dab42][6b8b2285c8ec]
6. **Avoid polymorphic function signatures that change behavior based on argument type or count ("functionarity").** They are harder to use correctly, especially in loosely-typed languages, and can quietly hide dangerous behavior behind an innocuous-looking call. Condition: especially dangerous when one of the possible behaviors is unsafe (e.g., allocates uninitialized memory) and looks identical at the call site to a safe one. [6b8b2285c8ec][b7d4c72be09c]
7. **A "leaky abstraction" - one that hides implementation detail except in rare edge cases - is a security risk precisely because developers never learn about the edge case until it bites them.** The more edge cases an abstraction has, the leakier and more dangerous it is. Condition: watch for framework "convenience" features (auto-handling HEAD requests, auto-checking CSRF only on POST) that quietly assume your code's shape. [f8b24497d8ed][ba7be98c2678][ba831619923d]
8. **Same-Origin Policy is defined by (protocol, hostname, port) only - never by IP address.** This is the single fact that makes DNS rebinding possible: a hostname's resolved IP can change mid-session without the browser treating that as a new origin. [c32f629c3361][5f3f955eca81][beb76ff27355]
9. **A server that authenticates callers purely by "can you reach me on this port/network" (no credential at all) is not actually authenticating anyone**, because DNS rebinding (for browser-originated attacks) and plain LAN access (for other attacks, e.g. Mirai) can both make an untrusted party "reach" it. Condition: applies to local HTTP servers, LAN-only admin tools, IoT-style devices, and any "trust by network position" design. [beb76ff27355][94f2b6b91c87][10ca40764a04]
10. **Ambient authority (the browser automatically attaching cookies to any request bound for a given domain, regardless of who initiated it) is the root mechanism behind CSRF.** SameSite cookies are the modern, low-error-rate fix; CSRF tokens are the older, equally effective but more error-prone (per-endpoint, easy to forget) fix that predates SameSite and still appears in real codebases. [9a7ac826028b][05aa24ef18f6][e734ff1cfc33]
11. **The Host header (which site the client believes it is connecting to) and the Origin header (which page's script is making the request) answer different questions and must not be confused.** Host-header validation is the correct, and only reliable, defense against DNS rebinding; checking Origin instead only affects whether a response can be *read*, not whether the request's side effects happen. Confusing the two produced a real, months-long unfixed vulnerability (WebTorrent case, section 7). [253ee935eb07][607192d0a0b8]
12. **Untested code is presumed broken.** The source states this as a near-absolute, not a nuanced trade-off, unlike its stance on cleverness. [dc285a9025b6]
13. **A large, unreviewed dependency tree is a standing trust decision, not a one-time install event.** A package's or extension's maintainer, and therefore its trustworthiness, can change after you've already adopted it (handoff, acquisition, account compromise) - install-time trust does not carry forward automatically. [58d9f7b5cc9d][d0dc40044d63][5bef1a8b8d76]

## 3. Procedures

### A. Defend a Node/Express-style local or internal HTTP server against DNS rebinding
1. Identify every endpoint reachable by `localhost`/loopback or a LAN address that a browser could conceivably reach (any local admin tool, sync helper, or device management UI your ecommerce ops team runs on a machine that also browses the web). [ab7590c804a1][8b445aa6c28b]
2. Add a single middleware that runs before every route handler and checks the request's `Host` header against the exact expected value (e.g. `localhost:8080`), not the `Origin` header. [607192d0a0b8][1a615ebaa111][253ee935eb07]
3. On mismatch, actively close/destroy the connection (or throw, causing the framework to reject it) - do not merely omit a CORS response header or return `false` from an "is this origin allowed" helper function. The source's own WebTorrent case shows that the latter looks fixed in testing but leaves the vulnerability live. [1a615ebaa111][beb76ff27355]
4. Bind the listener to the loopback interface explicitly (pass the host argument to `listen()`) as defense-in-depth against other-machine access - this does not stop DNS rebinding (which originates from the same machine's browser) but does reduce the separate, unrelated risk of direct network access. [52234a70e9a2][c6d9f612cf28]
5. If the design allows it, prefer not running a local HTTP server at all (e.g., register an OS-level custom URL protocol handler instead, so the OS prompts the user before launching your app) - the source's strongest recommendation, not always practical. [2bb630f6df7d]
6. Test the mitigation against a non-browser caller too (e.g. a raw script) to confirm the check is enforced independent of any browser behavior, since a local server is also reachable by non-browser processes that don't follow CORS/SOP rules at all. [b09187c3abe4]

### B. Defend a POST-only state-changing endpoint against the GitHub-style CSRF/HEAD bypass
1. Register GET and POST on distinct handlers/routes rather than one function with an `if request.get? ... else (treat as post)` pattern. [bc21e3deb98d5][83318b4ce2d8]
2. If a single function must remain, replace the two-branch if/else with an explicit `if get ... elsif post ... else raise/throw` - never assume only two method values are possible. [9b062a4c9cbf][fbdd4166ffd4]
3. Perform the CSRF-token check explicitly, immediately before the sensitive action, rather than relying solely on an implicit framework-level "before" filter that may only fire for one HTTP method. [b8c4d4acd19f][21e9f01540df]
4. Prefer SameSite=Lax (or Strict, if no legitimate top-level cross-site navigation is needed, e.g. OAuth login redirects) cookies over CSRF tokens as the primary defense; keep CSRF tokens as defense-in-depth for old browsers or enterprise contexts if needed. [0d2a5b6f2851][c2bad816cf64][1b76024d8b1a]

### C. Implement a stateless CSRF token (when SameSite cookies alone are not sufficient)
1. Generate the token as `HMAC(session_id, server_secret)` rather than a purely random value the server must remember. [dd0c8d03e16c]
2. Embed it as a hidden form field, echoed back on every state-changing submission. [dd0c8d03e16c]
3. Validate by recomputing the HMAC from the incoming session ID and comparing to the submitted token; reject on mismatch. [dd0c8d03e16c][48d54741b489]
4. Include it on every state-changing form (cart update, checkout, account edit) - a single forgotten endpoint reopens the hole. [dd0c8d03e16c]

### D. Validate JSON-derived user input safely
1. Check the TYPE of each field, not just its presence, before using it in a type-sensitive operation (e.g., before passing to a buffer/encoding constructor). The source's live demo showed that failing to check `typeof data.str === 'string'` let a caller substitute a number and trigger uninitialized-memory allocation instead of string conversion. [5178759551047][e9b008698c7a]
2. Prefer safe, explicit allocation APIs over a single polymorphic constructor whose behavior depends on argument type. [e9b008698c7a][6b8b2285c8ec]

### E. Reduce JavaScript-language footguns in storefront/checkout code
1. Add `"use strict"` at the top of relevant files/modules. [c4832f358c3b]
2. Install and run a linter (ESLint, or a preset such as "standard") on every commit; do not rely on memory of language edge cases. [c4832f358c3b]
3. Always use `===`, never bare `==`. [c4832f358c3b]
4. Call `Object.prototype.hasOwnProperty.call(obj, key)` instead of `obj.hasOwnProperty(key)` when `obj` may contain attacker-supplied JSON keys. [c4832f358c3b]
5. Do not rely on manually-placed semicolons alone to avoid Automatic Semicolon Insertion bugs (e.g. `return` followed by a newline then an object literal silently returns `undefined`); rely on the linter to flag the resulting unreachable code. [215a31ca49db]

## 4. Rules, thresholds and numbers

| Rule / fact | Number or threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| DNS TTL an attacker sets to force fast re-resolution | "order of seconds" | Attacker controls their own domain's DNS | Lecture description, not measured | [c6ab9bef1556] |
| Retry interval for a background rebinding attempt | roughly every 10 seconds | Attacker automating the attack post-page-load | Lecture description | [beb76ff27355] |
| Number of TCP ports an attacker could brute-force to find a local server | ~65,000 | Port unknown to attacker in advance | Lecture, order-of-magnitude claim | [c6ab9bef1556] |
| IoT device vulnerability to DNS rebinding, by category | 55% smart TVs, 66% printers, 75% IP cameras, 77% phones, 78% streaming/smart speakers, 87% routers/switches/APs | As surveyed by unnamed "security researchers," date not given in lecture | Secondhand citation `[web check: original study/date not named]` | [94f2b6b91c87][9ff2f352f40f] |
| GitHub OAuth CSRF-bypass bounty | "$25K," called the largest GitHub had paid at the time | Researcher's HackerOne report | Secondhand news story `[web check: verify exact figure/date]` | [af3509836f1a] |
| Time from GitHub bug report to fix | Acknowledged in ~8 minutes; fixed in ~3 hours | Same GitHub OAuth case | Lecture's retelling | [af3509836f1a] |
| WebTorrent DNS-rebinding bug, unnoticed after "fixed" | ~6 months | Fix checked Origin instead of Host in the wrong place | Presenter's first-hand account | [beb76ff27355][607192d0a0b8] |
| OpenSSL/Heartbleed-era annual donations to the sole maintainer | ~$2,000/year | As stated in post-Heartbleed reporting, year given as 2017 in lecture (likely misspoken; commonly reported as 2014) | Secondhand `[web check: verify figure and year]` | (no dedicated card found; see section 9) |
| Microsoft security-update vulnerabilities that were memory-safety issues | ~70% in a "recent" year | Cited Microsoft study, year not given | Secondhand `[web check]` | [cc9507377ff5] |
| Chrome all-time critical bugs vs. memory-corruption-unrelated | 130 total critical bugs; only 5 unrelated to memory corruption | Chrome's own bug data, as cited by lecture | Secondhand `[web check]` | [cc9507377ff5] |
| curl maintained largely by one hobbyist | ~20 years, then went full-time | As of lecture date | Lecture, unverified `[web check]` | (no dedicated card found; see section 9) |

## 5. Diagnostics and checks

- **Is a local/internal server vulnerable to DNS rebinding?** Check: does every handler validate the `Host` header against an exact expected value before processing? Good: mismatch closes the connection immediately, at the top of the request pipeline. Bad: no check at all, or a check that only withholds a CORS header (`Access-Control-Allow-Origin`) rather than rejecting the request. Fix: implement Procedure A above. [1a615ebaa111][253ee935eb07]
- **Is a POST-only sensitive action actually protected from HEAD/other-method bypass?** Check: are GET and POST routed to genuinely separate handlers, or merged into an if/else? Good: separate routes, or an explicit elsif/else-throw. Bad: a two-branch if/else assuming only 2 possible methods. Fix: Procedure B. [83318b4ce2d8][9b062a4c9cbf]
- **Is a buffer/encoding endpoint safe against uninitialized-memory disclosure?** Check: does the code validate the TYPE of every JSON field before it reaches an allocation/encoding call? Good: explicit `typeof` check on each field. Bad: any field's type is assumed rather than verified. Fix: Procedure D. [5178759551047][e9b008698c7a]
- **Is your team's dependency and browser-extension posture stale?** Check: when did you last confirm the current maintainer/owner of each critical dependency or installed browser extension, not just its reputation at install time? Bad: no process exists; trust was established once and never revisited. Fix: periodic dependency/extension audit. [58d9f7b5cc9d][d0dc40044d63] `[needs brand data: list of ecomOS/client dependencies and any staff-installed browser extensions to audit]`

## 6. Tools, settings and named features

- **`"use strict"`**: JS strict-mode pragma; catches duplicate function parameters, silent-to-loud error conversion, blocks octal-via-leading-zero, and turns undeclared-variable assignment into a runtime error. Does NOT catch duplicate object-literal keys or `hasOwnProperty` shadowing - only a linter does. [c4832f358c3b]
- **ESLint**: named as the most popular JS linter; "standard" named as a preset config the presenter personally created (disclosed bias) with an automatic fixer. [c4832f358c3b]
- **SameSite cookie attribute** (`Strict` / `Lax`): `Strict` withholds the cookie on any cross-site-originated request including legitimate top-level navigations; `Lax` allows the cookie on top-level navigations (e.g. clicking a "Login with X" button) but withholds it on background/subresource requests - the mode that preserves OAuth-style login flows while still blocking the CSRF-style forged background request. [0d2a5b6f2851][1b76024d8b1a] `[verify UI/spec: exact current SameSite default behavior per browser]`
- **CORS preflight (`OPTIONS`)**: browsers require it before sending "non-simple" cross-origin requests (custom headers, methods like PUT/DELETE, non-form content types); the server's OPTIONS response must explicitly allow the origin and method or the browser blocks the follow-up request. [f844ddaf9294][40f9a5454ce6]
- **Express `app.use` vs `app.get`/`app.post`**: naming a route with `app.get`/`app.post` restricts it to one method by construction; `app.use` explicitly signals "handles every method," which the source argues makes Express structurally less prone to the GitHub/Rails-style method-confusion bug. [bc21e3deb98d5]
- **Chrome's "Rule of Two"**: a named internal design heuristic - code should have at most 2 of (untrusted input, memory-unsafe language, high privilege); Chrome's renderer/browser-kernel process split is the applied result. `[web check: confirm this is still Chrome's stated current architecture principle]` [d88edc4583e1]
- **Site Isolation / CORB (Cross-Origin Read Blocking)**: Chrome features that put each site in its own process and block cross-origin responses from ever entering a renderer's memory when they could never legitimately be used as the requested resource type - a mitigation for both compromised-renderer and Spectre-class risk. No dedicated card found for these two specifically; covered under the general renderer/browser-process-separation card. [d88edc4583e1]
- **bcrypt**: recommended, low-effort, "just use it" password hashing library. [5d7219b293c0]

## 7. Examples and case results

All below are presented in the source as real, named incidents (not hypotheticals), except the live in-class demos, which are illustrative code the instructor wrote live.

- **GitHub OAuth "Authorize" CSRF bypass via HTTP HEAD**: a researcher found that GitHub's Rails-based OAuth authorize endpoint routed GET, POST, and (unbeknownst to the developer) HEAD requests through one controller's if/else, and that Rails' CSRF check only fired on POST. A bare HEAD request with the victim's ambient cookies silently authorized an attacker's OAuth app with zero user interaction. Example numbers: reported bounty ~$25K (largest GitHub had then paid), acknowledged in 8 minutes, fixed in 3 hours. Treat as an example, not a guarantee of GitHub's current behavior. [af3509836f1a][21e9f01540df]
- **Node.js Buffer uninitialized-memory disclosure demo**: a live-coded `/api/convert` endpoint that trusted a JSON field's type; passing a number instead of a string to the (old, unsafe) `new Buffer(n)` constructor returned raw uninitialized process memory, including a fragment that looked like Express's own source code, to the caller. Presented as structurally similar to Heartbleed. [5178759551047]
- **Blizzard Update Agent RCE via DNS rebinding**: a bundled local HTTP server accepted "download and execute this binary" commands from any caller because it never checked the Host header; DNS rebinding let any visited website trigger full remote code execution. Found by Google Project Zero; fixed. `[web check: confirm CVE/advisory]` [cfc30f6f66f17]
- **Transmission BitTorrent client RCE via DNS rebinding**: the backend daemon process accepted commands from any caller (not just its own UI), including endpoints that could execute arbitrary shell commands; DNS rebinding again gave RCE to any visited website. Also found by Google Project Zero. `[web check: confirm CVE/advisory]` [cfc30f6f66f17]
- **WebTorrent's own DNS-rebinding bug (presenter's first-hand account)**: after seeing the Transmission disclosure, the presenter audited their own project and found a real (though less severe - information disclosure, not RCE) DNS-rebinding bug. Their FIRST fix checked the Host header but inside an `isOriginAllowed()` function that only returned `false` (suppressing a CORS header) rather than closing the connection - this looked fixed but was not, for about 6 months, until a bounty hunter (paid "hundreds of dollars" via Brave's bug bounty, since WebTorrent code ships inside Brave) found it again. [beb76ff27355][607192d0a0b8]
- **Mirai botnet**: teenagers compromised a large number of internet-facing IoT devices (no DNS rebinding involved - devices were directly reachable with no firewall, or used default admin/admin credentials) originally to attack a rival Minecraft server's host/DNS provider. Included Russian-language strings to misdirect attribution and deliberately avoided attacking DoD/HP/GE IP ranges. `[web check: verify attribution details]` [10ca40764a04]
- **2014 Chrome buffer-overflow via `__defineGetter__`**: plain, unprivileged JavaScript overrode a small buffer's reported `byteLength` via a getter, tricking Chrome's C++ engine into treating it as much larger, enabling arbitrary read/write of the browser process's memory from an ~6KB exploit. `[web check: identify the specific research/CVE]` (no dedicated card found)
- **npm malicious-maintainer-handoff incident**: a prolific maintainer ("Dominic," ~700 packages) handed off publish rights to a package he'd stopped using, per normal open-source practice; the new co-maintainer added malware as an encrypted, runtime-`eval`'d string whose decryption key was derived from the parent package's own metadata - so it activated only for one specific downstream target (a Bitcoin wallet), exfiltrating its private keys once balance exceeded a threshold. Strongly resembles the widely-reported "event-stream"/Copay incident (~Nov 2018) but is not named explicitly in the transcript. [d0dc40044d63] `[web check: confirm exact incident name/date before citing publicly]`
- **Accidental npm install-script `rm` incident** ("bumblebee," per a student's unconfirmed naming): a stray extra space in an `rm` command inside a package's install script caused it to delete a whole system-binaries directory on every installing machine - an honest mistake with severe impact. `[web check: confirm package/incident name]` (no dedicated card found)

## 8. Mistakes the source warns about

- Merging multiple HTTP methods' handling into one function/branch instead of separate routes. [bc21e3deb98d5][9b062a4c9cbf]
- Relying on an implicit, framework-level CSRF check that only fires for one method (e.g. POST) instead of validating explicitly at the point of the sensitive action. [b8c4d4acd19f][21e9f01540df]
- Checking the Origin header when you mean to check the Host header (or vice versa) - they answer different questions. [253ee935eb07]
- "Fixing" a security check by only suppressing a response header (e.g., returning `false` from an "origin allowed" helper) instead of actively rejecting/closing the request. [beb76ff27355]
- Trusting the declared/assumed type of a JSON field instead of validating it, especially before passing it into a type-sensitive API like a buffer constructor. [5178759551047]
- Designing an API whose insecure use is the easy/default path. [0021606dab42]
- Designing a function whose behavior silently changes based on argument type or count (polymorphism/arity tricks), especially when one behavior is dangerous. [6b8b2285c8ec][b7d4c72be09c]
- Binding a server to all network interfaces by default instead of loopback-only, when only local access is intended. [c6d9f612cf28][52234a70e9a2]
- Assuming network position (LAN-only, loopback-only) is sufficient authentication for a local/internal service - it is not, because of DNS rebinding and, separately, other LAN-resident threats. [beb76ff27355][94f2b6b91c87]
- Writing "too clever" code (short-circuit control flow instead of `if`, obscure prototype/`call`/`apply` tricks, dense one-liners) that costs reviewers (including the original author, later) significant time to understand, or hides which branch actually runs. [613fd4e14efd]
- Shipping code without automated tests and trusting a manual read-through instead. [dc285a9025b6]
- Assuming a dependency's or browser extension's trustworthiness at install time still holds later, without re-checking who currently maintains/owns it. [58d9f7b5cc9d][d0dc40044d63]
- Logging an unexpected/unhandled exception and continuing to run instead of crashing the process, when the failure was not one you wrote code to expect. [0fd2f1e28cc1][633153c6724d]

## 9. Caveats, conflicts and what is missing

- The source itself flags several of its own numbers as "the way you'd experience this may vary" (DNS cache TTL enforcement varies by resolver; some ISPs enforce a floor well above what an attacker requests, so an attack that "should" take seconds might take up to ~10 minutes or fail to reliably succeed). [c6ab9bef1556]
- The Heartbleed year given in the lecture (2017) does not match the almost-universally reported 2014 public disclosure date; this is very likely a lecturer's misstatement rather than a documented alternate fact. Flagged as `[web check]` rather than corrected outright, per instructions not to invent facts the source didn't give.
- No dedicated card in the supplied card set was found specifically for: the 2014 Chrome buffer-overflow-via-getter research, the OpenSSL/Heartbleed maintainer-funding story, or the curl hobbyist-maintainer story, or the accidental `rm`/install-script incident - these are covered in this mini playbook's prose (sections 7-8) but not independently cited to a card id; treat them as thinly sourced pending a card review, or as content that may live in a different part of this same source.
- The source explicitly frames "don't be overly clever" and reverse-indentation-as-art as matters of taste, not hard security rules - do not upgrade that to an absolute law when merging into the folder playbook.
- The source gives no concrete guidance on exactly how to detect a DNS-rebinding attempt short of the Host-header check; it explicitly rejects several alternatives (framework-level detection via function introspection, requiring HEAD requests to also carry CSRF tokens, refusing to auto-handle HEAD at all) as impractical or costly, without offering a fully worked replacement beyond "check Host and reject on mismatch." Treat Host-header validation as the one concrete, source-endorsed control; anything beyond it (e.g. resolver-level blocking of DNS answers pointing at loopback/private ranges) is mentioned as a possibility a student raised, not something the source confirms is deployed or effective at scale. [14b6536a8fe7]
- This part does not cover pricing, current UI steps for any platform, or ecommerce-platform-specific settings (e.g., no Shopify/WooCommerce-specific material appears in this part) - that gap should be filled from other sources in this folder, not invented here.

## 10. Card index

Cards cited from this part (24-character id, title). Some ids may also be cited by other parts of this same source if the underlying lecture material spans a part boundary; that overlap is expected and not an error.

- 91d7cee32897f4434d78cd90 - Map your ecommerce attack surface by target: browser, server, client app, user
- f4015dad3b23e8f569f6e8c0 - Set Secure, HttpOnly and SameSite on Session Cookies
- 1b76024d8b1a18e44896bf5c - SameSite Lax versus Strict: Choose by Funnel Impact
- 0279d922e7225195b39f10d9 - Set SameSite on Session Cookies to Stop Ambient Cross-Site Requests
- f56b85f95c18505d7bf7f4fb - Layer CSRF defenses on authenticated store actions
- 638455ba94533852f78674de - GET-request and CSRF exposure in storefront logout and account actions
- c2bad816cf64735e1ba0958e - Use SameSite cookies to block cross-site state-changing requests
- 9a7ac826028be112b75c211a - CSRF fundamentals: ambient cookie authority and forged state-changing requests
- dd0c8d03e16ce2d8c90e2273 - Implement stateless CSRF tokens with HMAC over the session ID
- 48d54741b489b3210f08e18d - Why the CSRF token defeats a forged request: same-origin policy blocks token theft
- 83318b4ce2d8d93fdf169d19 - Method-specific routes prevent CSRF bypass via HEAD
- 925578938d71929331e96844 - CSRF defense for storefront authenticated actions
- 21e9f01540df35d6e368a6c9 - CSRF token bypass via HTTP HEAD and framework magic
- 0d2a5b6f2851e489fdf77233 - SameSite strict vs lax: don't break OAuth login on your storefront
- b8c4d4acd19f74d5b3223745 - Add CSRF Validation Centrally for State-Changing Requests
- 05aa24ef18f6e79914f347c4 - Ambient Authority via Cookies: Use SameSite
- e734ff1cfc33993e2ffe0278 - Recognize ambient authority and its limits
- 43566cfc761f4b2c3e13c0d7 - Governing agent and integration access with OAuth scopes
- 490bcd204080046a3b491bfa - Use the Host header to route multi-tenant or multi-store requests
- d0eca305c2e69bd1c25ab544 - Reject Cross-Site Form Submissions Using Origin Header
- c32f629c3361719207aa29b8 - Capabilities of a same-origin rebinding-style attack on storefronts
- beb76ff27355a79d059df754 - DNS Rebinding: How an Attacker Turns a Visitor's Browser into a Proxy for Your Local Services
- 607192d0a0b8a60dec0fa2bc - Host Header Validation: The Standard Server-Side Defense Against DNS Rebinding
- caf8a153db5fe3aa3126f1f9 - Rebinding Against Remote HTTPS Sites Is Largely Blunted by TLS and Cookies
- c6ab9bef15567d28f920dff1 - Caching and Keep-Alive Timing Determine Whether Rebinding Succeeds at All
- cfc30f6f66f17d185bf4668a - Real DNS Rebinding Incidents Show the Blast Radius: Update Agents and Background Daemons
- 31b04866d31bc397d9a7cd64 - Run a Bounded Rebinding Test Against Your Own Local Service
- 253ee935eb076a75d2d2e50a - Host vs Origin Headers: Keeping the Two Checks Straight in Store Integrations
- ab7590c804a160420cc810d6 - Reduce the Local-Server Attack Surface Before Adding Detection
- 14b6536a8fe742d481dec7a2 - Resolver-Level Mitigation: Refusing DNS Answers That Point to Loopback or Private Ranges
- 5f3f955eca81ccf53d35bdb4 - Hostname-to-IP reassociation is the mechanism to explain in store risk reviews
- b09187c3abe4d8c8bd7fa0e8 - Validate the mitigation against non-browser callers too
- 1a615ebaa111bd7ba7a6184a - Enforce the Host Check at the Very Top of the Request Pipeline
- 2bb630f6df7d95bbdc98475b - Decide How Much Local-Server Functionality Your Product Actually Needs
- 8b445aa6c28be948e9ad8261 - Scope local-network and integration endpoints so a browser cannot reach them
- 2cadaaa9061407b985112ec7 - Give each listener its own port and verify the actual request on the wire
- b4c4297cd2c3a0699814671b - User interaction before a sensitive local or remote action
- 40f9a5454ce6c953349bc4f9 - Use non-simple requests as a defense in depth, not as the fix
- f844ddaf929484dd697579c9 - Simple vs preflighted requests: which cross-site calls a page can make
- 8764cd07524b998029c71190 - Keep access-control headers off endpoints that never meant to share data
- bd043182fa5a6c2b516bdb8b - Use allowlist identity keys and reject unauthenticated state changes
- 27dfeb1d3d4e41cc251bb7ee - Treat agent- and browser-initiated requests as untrusted input, not authorization
- 94f2b6b91c876288807a8d6d - Prioritize router and network-device exposure in the store environment
- 9ff2f352f40f41df418904fd - Monitor inbound reachability and device updateability on the store local network
- 10ca40764a04813e3ee1abb7 - Mirai as an Ecommerce-IoT Cautionary Case: Default Credentials and Internet-Facing Device Ports
- c3761e03321cd490dfc6b127 - Bound Session Reuse of Local Admin Tools in Store Operations
- c7cb2f7d9bcdf6b60e818b12 - Browser Engine Bugs Let Merely Visiting a Page Compromise the Machine
- eac31cbbcd3c1f4043c66b00 - Assume Breach at the Browser Layer and Design Store Systems for Containment
- 5178759551047b58dc47a9b0 - Uninitialized-buffer disclosure: prevent leaking memory from user input
- e9b008698c7ab582f2c81249 - Secure Binary/Buffer Encoding Endpoints Against Memory Disclosure
- 4b80b29f09b698b345f22249 - Treat memory disclosure and uninitialized buffers as a storefront data-leak risk
- cc9507377ff5fcc7054253a7 - Defend against memory-safety bugs as the dominant vulnerability class
- 30411f850269439713dc634f - Serve large files as streams instead of buffering
- 52234a70e9a2abe7977ceea0 - Bind listeners to the intended interface
- c6d9f612cf285de6bc213f9d - Never Bind Servers to All Interfaces by Default
- f8b24497d8edb3541bebc0bb - Fix leaky abstractions that hide security-relevant detail
- 6b8b2285c8ec7ae6e6e812fc - Avoid APIs with insecure defaults or polymorphic signatures
- ba7be98c2678f99c0c80417d - Leaky abstractions in frameworks cause security bugs
- ba831619923db9063190ff35 - Treat Leaky Abstractions as Likely Edge-Case Holes in Store Code
- 47019286e6cf3be2ce9cab62 - Reduce Component Interactions, Not Just Component Count
- c4e441b6c91e51d9e89dd910 - Design-time checklist for reducing server complexity
- 613fd4e14efdf0fb2d924715 - Use Explicit Code Over Clever Code in Security-Relevant Paths
- 633153c6724dedb4944b5f20 - Fail Early on Unexpected State; Handle Expected Errors Gracefully
- 0fd2f1e28cc178298ac2ce25 - Fail fast when an assumption is violated
- fbdd4166ffd478219c49b95d - Assume Inputs Are Wrong: Verify Assumptions at the Top of Each Function
- 76589f02571278fe770785fe - Defensive coding: assert assumptions and fail closed on sensitive actions
- 0021606dab420a68f12673df - Reject APIs Whose Insecure Path Is the Easy Path
- b7d4c72be09ca227cb516680 - Watch for Hidden Behavioral Switches in Function Signatures
- 9b062a4c9cbf96cadb22cc34 - Defensively whitelist HTTP methods in store endpoints
- bc21e3deb98d58b887c1e733 - Split storefront routes by HTTP method and purpose
- 4826df0e2362ffcc30004823 - Use Strongly Typed Checks to Force Exhaustive Case Handling
- d88edc4583e14a2c18f0dc5d - Renderer/browser process separation to limit storefront breach damage
- c4832f358c3b208f153e0a33 - Harden JavaScript for storefront and checkout code
- 215a31ca49db18c0fd2a49e2 - Defend against automatic semicolon insertion pitfalls in storefront scripts
- dabc409377d8ac80ceec5278 - Prefer explicit, boring code over clever code in security-relevant paths
- 708eeab33a81ed123b47b074 - Prefer Explicit Code Over Clever Code in Store Systems
- 3465725696aa2a77fdcbc48f - Make Dangerous Code Look Dangerous
- 6e3562b35c0b53bfa999c11c - Adopt a Paranoid, Vigilant Security Mindset
- cfeef85a65fb2f16bb26b4a6 - Apply defense-in-depth and a paranoid mindset to storefront security
- 103d992322b16d85fe847aa4 - Defense-in-Depth: Assume the Password Is Already Compromised
- 5d7219b293c0ceb222a97141 - Store passwords with a maintained adaptive password hasher
- dc285a9025b6d13302e430f8 - Write tests because untested code is broken code
- 58d9f7b5cc9d26d6e3068799 - Protect against the open-source and extension supply chain
- d0dc40044d63debfc0dab5a8 - Recognize targeted dependency attacks and account-takeover risk
- 5bef1a8b8d767ad450b09053 - Smaller Packages Have Enlarged Modern Dependency Trees
- cd71b97b8356c4041a6fc1fd - Standardized Collaboration Platforms Accelerated Code Flow
- 4eebd777221695d9b3a575ef - Enforce strong auto-update for storefront dependencies
- af3509836f1a8c8a44e0e7f0 - Security researcher case studies: read disclosed vulnerabilities as learning material
- 71d76aebc126a2e69ce427e0 - Prefer simple browser-level security over repeated per-app logic
