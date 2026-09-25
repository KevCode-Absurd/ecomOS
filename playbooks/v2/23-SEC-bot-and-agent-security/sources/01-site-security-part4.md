# Site Security (part 4 of 5)

source_id: 1NR2jtUMB0KkTlV_QTIGSmWVT-je-24Pt  |  folder: 23-SEC-bot-and-agent-security  |  cards: 326 total for the whole source (this part cites the subset below, drawn mostly from the range covering authentication, WebAuthn, Node.js vulnerability process, and CSRF/HEAD-request framework bugs)  |  words: this part is ~53,900 of the source's 273,439 total  |  type: university course transcript (recorded lecture series) plus two embedded guest-lecture transcripts

**Part note:** this is one of 5 equal text-part splits of one oversize source, covering only the words in this part. A later merge agent combines parts 1-5 into one mini playbook for the whole source. This part opens mid-lecture on password/authentication security, continues through a guest lecture on WebAuthn/FIDO2 (speaker: Lucas Garron, GitHub security engineer, ex-Chrome security team), then a guest lecture on Node.js project security (speaker: Miles Borins, Google Developer Advocate and Node.js Technical Steering Committee member), then opens a new lecture reviewing CSRF and ends mid-explanation of a real GitHub OAuth account-takeover bug caused by an HTTP HEAD-request bypass. Topics covered in this part: authentication vs. authorization; password policy, storage, hashing, salting and bcrypt; breach data and Have I Been Pwned; network-based credential-guessing attacks and their defenses (rate limiting, CAPTCHA, step-up re-authentication, response-discrepancy/timing side channels); multi-factor authentication and TOTP/HOTP; WebAuthn/FIDO2 in depth; Node.js project vulnerability process (MITRE/CWE/CVE/CVSS, embargoes, HackerOne, the Internet Bug Bounty, worked CVE case studies, semver-vs-security policy, LTS constraints, npm/supply-chain risk, serverless threat models); and CSRF fundamentals plus a full case study of a GitHub OAuth CSRF-bypass vulnerability and the "leaky abstraction" lesson it teaches. Topics NOT covered in this part (they belong to other parts of this same source): SQL injection detail, XSS detail, the opening framing of the course, and whatever the lecture moves on to immediately after the "leaky abstraction" explanation (part 5 should pick up there).

credibility: A recorded university-course lecture series (unnamed institution and instructor in the text itself, but internal references — "CS253", guest lecturers introduced as friends/former colleagues of the instructor, a mention of "Ferris" as a co-instructor, references to Stanford student email/coursework, a Stanford Bug Bounty Program, and CS107/CS253-style framing) place this as a Stanford web-security course transcript. `[web check: confirm exact course number/instructor name if attribution matters]`. The main lecturer teaches from general web-security knowledge, textbook-style advice (NIST guidelines, OWASP-adjacent concepts) and some personal anecdotes; no first-party company data of his own is presented. Two guest lecturers bring first-party professional experience: Lucas Garron speaks as a GitHub security engineer building WebAuthn support and a former Chrome security-team member (badssl.com, HSTS preload list), giving his own professional opinions, explicitly flagged as personal ("not officially GitHub's/Google's position" is implied by his own framing, especially around the ICE-contract discussion). Miles Borins speaks as a Google Developer Advocate and a member of the Node.js Technical Steering Committee with hands-on responsibility for Node.js security releases, and states explicitly that his opinions are his own, not Google's. All three speakers give real operational detail (Node.js's actual embargo policy, HackerOne response times, worked CVEs) mixed with some personal anecdotes, hedged guesses ("I don't know," "I'd have to look that up") and a few unverified/undated claims (a Pastebin breach-sale anecdote, a "hash-wick" vulnerability name that is unclear in the transcript). Treat named vendor/product claims and specific dated statistics as `[web check]` before repeating them as current fact.

date signals: Internal references date the two guest lectures to specific points: the WebAuthn talk references WebAuthn having "launched around August" (year not stated in this excerpt) and discusses "recent" reCAPTCHA and browser support state; the Node.js talk explicitly says "the current cost... as of July 2019" for a cited Microsoft cracking-cost figure, references Node versions 8, 10, 12 and 13 as concurrently maintained (dates this specifically to late 2019, since Node 13 shipped October 2019 `[web check]`), and references "this year" having only 3 security releases versus "a lot more in 2018," implying the talk was given in 2019. The CSRF/GitHub-OAuth lecture references a HackerOne report resolved "2 weeks ago" relative to the lecture and Node.js content ("remember Miles talked about last time"), placing it shortly after the Node.js talk, so also circa late 2019. Overall this part's content should be treated as circa-2019 web-security teaching material: still broadly correct on fundamentals (password hashing, CSRF, CVE/CWE vocabulary) but any named tool, vendor feature, browser support matrix, or "current" statistic needs a fresh `[web check]` before being treated as true today.

## 1. What this source is for

Gives a builder of a web application (explicitly including e-commerce-relevant flows: login, password reset, checkout-adjacent sensitive actions, third-party OAuth integrations) a from-first-principles understanding of how to implement authentication safely, how modern multi-factor and passwordless authentication (WebAuthn/FIDO2) actually works and where it still falls short, how a real open-source project (Node.js) runs its vulnerability-disclosure and patching process end to end, and how a subtle framework behavior (auto-handling of HTTP HEAD requests) can silently defeat a CSRF defense — illustrated with a real, dated GitHub account-takeover bug. It is written to be actionable at the code level (specific library calls, specific `if`/`else` bugs, specific HTTP semantics) rather than as a policy or compliance document.

## 2. Principles

1. **Keep authentication and authorization strictly separate.** Authentication verifies who a user is (login form, cookie, biometric, possession of a device). Authorization decides, once identity is known, what that user may do (an ACL, or a capability such as a Google Docs URL token). Per NIST guidance cited in the source, authentication does not determine authorization or access privileges. Never issue a token that itself asserts "this user may do X" — issue a session ID and look up authorization on each request, so privileges can be revoked or changed without needing to revoke a signed claim. [de68d498e431] [d63cc78167711]

2. **Username handling must be case-insensitive for matching but preserve the user's chosen display case.** Store a lowercased column for uniqueness/lookup and a separate preferred-case column for display; compare login attempts against the lowercased column. Applies to any system letting users choose a username/handle. [9b569cd2522a]

3. **Password complexity rules are outdated; length and breach-checking work better.** Forced periodic rotation and forced upper/lower/number/symbol combinations do not produce stronger real-world passwords — users route around them predictably. Current NIST-aligned guidance: allow long passwords (up to 64 characters), enforce a minimum (8 is called "the bare minimum," itself still low), do not force rotation, and check new passwords against known-breach lists instead of imposing composition rules. Condition: applies to any password-based login; does not apply once a service moves fully to WebAuthn/passkeys (principle 12). [81c60e09127fe]

4. **Multi-word passphrases beat character-substitution passwords for equal or less user effort.** Four random dictionary words (even lowercase, unpunctuated) carry more entropy than a shorter password with symbol/number substitutions, per the source's cited entropy comparison (referencing the well-known "correct horse battery staple" argument). Recommend this to users who don't use a password manager. [813fb79b2bef]

5. **Never store passwords in plaintext or with a fast, unsalted hash; use a maintained adaptive hasher (bcrypt or equivalent).** A cryptographic hash function used for passwords should be deliberately slow, not fast. Unsalted hashing (even with a strong function like SHA-256) leaks which users share a password and is vulnerable to precomputed lookup-table attacks; salting (a random per-user value combined with the password before hashing, stored alongside the hash in plaintext) defeats both. bcrypt handles salting and adjustable work-factor automatically. Gotcha: bcrypt truncates input at 72 ASCII characters, so a policy allowing longer or Unicode/emoji passwords must pre-hash with another function before handing the result to bcrypt, or the extra length/characters are silently discarded. [9d8f903b4f27] [5d7219b293c0]

6. **Even with correct hashing, assume the attacker will recover a meaningful share of real passwords once a database is breached — because they attack with real breached-password corpora, not blind brute force.** A cited Microsoft estimate: a $20,000 machine could attempt about 100 billion SHA-256 hashes/second (as of ~July 2019); starting from real breached plaintext passwords alone can crack roughly 70% of a typical user base's passwords, because people are not very creative. This is the source's stated justification for principle 11 (assume the password is already known) rather than trying to make passwords alone unbreakable. [813fb79b2bef] `[web check: figure and year]`

7. **A strong password only protects against guessing and brute force — nothing else.** It does not protect against password reuse plus another site's breach (credential stuffing), phishing, man-in-the-middle interception, malware/keyloggers, coercion, or a password physically written down and found. Conclusion stated directly by the source: "passwords alone are not enough." [385b678a734e]

8. **Layer defenses against network-based guessing: rate limiting, lockouts, and CAPTCHA, with realistic expectations about CAPTCHA's limits.** Brute force, credential stuffing, and password spraying are the three named guessing-attack patterns; they differ in whether they target one account with many passwords (brute force), reused breach data across sites (credential stuffing), or one weak password sprayed across many accounts (password spraying). CAPTCHA and reCAPTCHA-style reputation scoring raise cost but are explicitly not unbreakable (evidence in section 7). [f753de594e48] [115d25c9c19d] [b6026850aadf] [00647bf08fc4]

9. **Generic, identical error messages defend against account enumeration — at a real usability cost that must be weighed against the sensitivity of the service.** Distinguishing "no such user" from "wrong password" (or a differing HTTP status code, or a differing response time) lets an attacker enumerate which emails/usernames have accounts on your service. Apply the same generic message across login, password reset, and account creation, not just login. The cost (frustrated legitimate users who forget which email they used) is explicitly framed as a trade-off, sized to how damaging enumeration would be for that specific service (source's own worked example: a bank, where confirmed-customer lists materially improve phishing). [83bd8b5f52f4]

10. **Timing differences between code paths are their own information-exposure side channel and must be closed by doing equal work on every path, not by fixing messages alone.** If a "user does not exist" path returns early while a "user exists" path performs a hash + database lookup, the measurable time difference alone reveals which is true, independent of the response text. Fix by performing the same hash-and-lookup work unconditionally and branching only at the end. [d3e7e7ef57e6]

11. **Design for the case where the attacker already has the user's correct password.** A cited (unverified) Microsoft claim: enabling MFA makes an account roughly 99.9% less likely to be compromised. Since breach-derived credential stuffing, phishing, and malware can hand an attacker a real password regardless of its strength, require or strongly encourage a second factor, scaled to service sensitivity (mandatory for financial-grade services, encouraged otherwise). [103d992322b16] `[web check: 99.9% figure/source]`

12. **Passkeys/WebAuthn intentionally stop modeling authenticators by "factor type" and instead treat every authenticator as a public-key challenge-response endpoint.** The traditional "something you know / have / are" framework breaks down at the edges (illustrated with an anecdote about a mathematician who used a mental day-of-week calculation as his own unlock mechanism). WebAuthn's `navigator.credentials.create()`/`.get()` abstracts over passwords, biometrics, hardware keys and platform authenticators (Touch ID, Windows Hello) uniformly, all backed by public-key cryptography, so implementers should design to that interface rather than to a specific factor category. [a55298b2b401] [cb2bba93c89d]

13. **A hardware-bound or platform-bound authenticator is materially stronger against phishing/relay than any code the user reads and re-types (SMS, TOTP, push notification, QR login), because the private key never leaves the device and a live physical action (tap, biometric) is required per authentication.** SMS and push notifications are explicitly rated weaker: they are code/approval mechanisms that a real-time relay/MITM attacker can pass through, and SMS specifically is further exposed to carrier-side account takeover independent of any active login attempt. TOTP is offline-capable and better than SMS but the 6-digit value itself can still be read, phished, or relayed by anyone who sees it. [9e5baf9f66b1] [b7540e558ff6] [9560f29c325a]

14. **Anti-phishing "security images"/knowledge-based security questions are not real security factors and should not be used or trusted.** They are meant to let the user verify the site, not vice versa, so they do nothing against a real-time relay attacker who simply fetches and re-displays the real image/response; a cited study found 72% of users still entered their password even when the image/caption was removed entirely. Positive UI indicators are commonly ignored by users. [b6d76d1c801a] [c16584de911d]

15. **Account recovery design is a hard, unsolved trade-off between recoverability and phishing/takeover resistance, and must be decided before enforcing strong factors, not after.** The more recovery flexibility offered (SMS fallback, support-desk identity questions), the weaker the overall guarantee, since security is only as strong as the weakest accepted recovery path. Some services (Google's Advanced Protection Program, cited generically) allow opting into "hardware keys only, no fallback," accepting permanent lockout risk as the trade-off for maximum takeover resistance. [822b4433112b]

16. **Threat-model the whole domain your project depends on, not just your own source code.** The source's own worked example: a Node.js project subdomain (`registry.nodejs.org`) was takeover-able via an abandoned CNAME record pointing to a third-party CDN that didn't verify domain ownership before letting anyone claim it — a DNS/infrastructure misconfiguration, not a software bug, that a good-faith researcher reported before it could be abused. [a1984ffa45bb]

17. **Use CVE, CWE and CVSS as a shared, portable vocabulary for classifying and scoring vulnerabilities, but re-score severity for your own deployment context.** CWE classifies the type of weakness; CVE identifies a specific found instance, scored by CVSS across attack vector, complexity, privileges required, user interaction, scope, and confidentiality/integrity/availability impact. The source's explicit caveat: CVSS reflects a generic threat model, and a high generic score does not automatically mean the same severity applies to your specific system. [0ef686a163b4]

18. **A coordinated-disclosure embargo needs an explicit policy, and that policy must bind the reporters/triagers even against their own employer's interest.** Node.js's real policy: every report is embargoed until public disclosure, and a security-team member cannot tell even their own employer (who may run Node.js in production) before disclosure — the source states plainly this rule has been broken at least once, giving one company an unfair advantage over other vendors. [20e8867f0d35]

19. **A security fix that breaks compatibility can and should ship as a minor/patch release rather than waiting for the next major version, when the alternative is leaving users exposed.** Node.js's own semver policy states security fixes are allowed to break the normal versioning discipline. Condition: this is Node.js's specific policy choice, not a universal semver rule — document your own project's equivalent policy explicitly rather than assuming it. [e19ee93824c2] (see also section 4 for the worked CVE example)

20. **`npm install` (and equivalent package-manager installs) is by design a remote-code-execution surface, because lifecycle hooks (e.g. post-install scripts) run arbitrary code for every dependency automatically.** The risk is entirely about where the install runs: inside a disposable, network-restricted sandbox (e.g. an ephemeral CI container building a Docker image) it is low-risk; run directly and unsandboxed on a persistent production host it can compromise that host outright if any transitive dependency turns out malicious. [6ada3852334a]

21. **Supply-chain trust cannot be fully solved by code review of the public source repository alone; the published package artifact can differ from what's on GitHub.** Worked case: the `event-stream` npm package attack embedded a payload only in the published npm tarball (not in the GitHub repo or its tarball), and made the payload decode only when installed at the exact expected dependency-tree depth of one targeted Bitcoin-wallet package, evading casual review entirely. The concrete mitigation the source highlights as one that would have stopped this specific attack: network-restricting the sandbox that runs the install, so exfiltration has nowhere to go, even without detecting the malicious code. [f5ed3504c3e1]

22. **An overly strict, high-friction security/compliance process is itself a security vulnerability, because developers will route around unusable process rather than accept lost velocity.** Stated directly by the Node.js speaker, drawing on Google's internal open-source compliance process: "creating a poor developer experience through trying to lock down your systems could actually make you less secure" — arguably the highest vulnerability an organization can create for itself. Recommended pragmatic pattern: let developers use anything in an isolated dev environment, then run a full dependency review only at promotion-to-production, flagging specific disallowed APIs/packages rather than banning broad categories upfront.

23. **Threat models must be re-derived per deployment environment, because the same platform can carry entirely different risks depending on how it's hosted.** Worked contrast: a shared, long-lived VM's main availability risk is classic multi-tenant resource-exhaustion DoS; a serverless/FaaS platform (example: Google Cloud Functions) isolates each request to its own instance, largely neutralizing that risk, but introduces a new one — a cost-exhaustion attack, where an attacker drives up the target's cloud bill by repeatedly triggering near-max-duration executions at scale, without ever taking the service offline. `[needs brand data: hosting model]` — this rule only applies once you know which deployment model your store's backend actually uses.

24. **CSRF exploits the browser's "ambient authority" cookie model: a request's cookies are attached based on destination domain alone, regardless of which site initiated the request.** If attacker.com can cause the victim's browser to send a request to victim.com, victim.com's session cookie is still attached, and the server alone cannot distinguish that from a legitimate same-site request. [9a7ac826028b]

25. **SameSite cookies are the primary, browser-enforced modern fix for CSRF; CSRF tokens are the pre-SameSite-era workaround, still needed for legacy browser support and still extremely common in real codebases.** A CSRF token (a server-issued nonce that must be echoed back on state-changing requests) works because an attacker's cross-origin script cannot read it out of the victim page's DOM (same-origin policy), even though the attacker can forge a request with the victim's cookie attached. Stateless implementation: derive the token via HMAC over the session ID plus a server-only secret, so nothing needs to be stored separately. [dd0c8d03e16c] [48d54741b489] [0279d922e722] [c2bad816cf64]

26. **SameSite=Strict can break a legitimate cross-site OAuth-style login flow; SameSite=Lax is the practical choice because it still allows a cookie on a genuine top-level browser navigation (the whole tab navigating), which is exactly what a real "Login with X" redirect is.** This is also why real OAuth "Login with Google/Twitter" flows always force a full top-level page redirect to the identity provider's own domain, even for apps requesting minimal permissions — that top-level-navigation requirement is what lets SameSite=Lax still work for the legitimate case while blocking hidden cross-site forgery. [0d2a5b6f2851] [1b76024d8b1a]

27. **A framework's automatic, "helpful" handling of an HTTP method (e.g. auto-routing HEAD requests through GET handlers) is a leaky abstraction that can silently defeat a security check written assuming only two methods are possible.** The worked GitHub case: `request.get?` returns false for a HEAD request even though Rails silently routes HEAD into the same controller code as GET, so an `if request.get? ... else` branch written to mean "else it's POST" actually also catches HEAD — and Rails' separate CSRF-check hook only fires "if POST," so it's skipped for HEAD too, letting a single unauthenticated-looking HEAD request grant full OAuth account authorization with no CSRF token at all. [21e9f01540df] [ba7be98c2678] [f8b24497d8ed] [83318b4ce2d8]

28. **Defensive coding for security-critical branches: enumerate every expected case explicitly and fail loudly (crash/throw) on anything unexpected, rather than letting an `else` silently absorb an unanticipated case.** Rewrite a two-way `if/else` as `if GET ... elsif POST ... else raise`. A crash is a bounded, alertable availability hit; a silent security bypass is not. Framework design implication: if a framework auto-routes one method into another's handler for convenience, it should also lie consistently to the developer's method-check calls (report the aliased method, not the true one), so the abstraction doesn't leak. [0fd2f1e28cc1] [76589f02571f] [9b062a4c9cbf] [ba831619923d]

## 3. Procedures

**A. Hash and store a new password (bcrypt pattern, the source's recommended default).**
1. Receive the plaintext password from the registration/change-password form.
2. Check the candidate password against a known-breach password list (e.g. an HIBP-style API/dataset) before accepting it; reject or warn if found. [e67276b1419] [d6e5ce45fe0]
3. If the site allows very long or Unicode/emoji passwords, pre-hash the plaintext with a general-purpose hash function first, to avoid bcrypt's 72-ASCII-character truncation silently dropping entropy. `[verify UI: your bcrypt library's exact truncation behavior]`
4. Call the bcrypt hashing function with the (possibly pre-hashed) password and a chosen work-factor/round count (source's example: 10 rounds) — bcrypt generates and embeds its own random salt in the output.
5. Store only the single returned bcrypt string (it encodes algorithm identifier, work factor, salt and hash together) in the database. Never store the plaintext or an intermediate unsalted hash.
6. To verify a later login attempt, pass the submitted plaintext (with the same pre-hash step, if used) and the stored bcrypt string to the library's own "compare" function — do not hand-parse the stored string yourself.

**B. Defend a login/authentication endpoint against network-based guessing.**
1. Wrap the authentication route in rate-limiting middleware (example named: Express Rate Limit for Node/Express) that tracks attempts per username and/or per source IP within a time window. [a84a0c3caf46]
2. Set the threshold using the source's rule of thumb: roughly an order of magnitude above the most extreme plausible legitimate rate (accounting for shared/NAT IPs, e.g. a corporate network), then raise it if legitimate users get blocked — bots will still exceed even a generous limit.
3. On detected abuse, either delay the response or return an explicit rate-limit HTTP error; do not silently succeed or fail differently based on correctness of the guess (see procedure D).
4. Optionally gate continued attempts behind a CAPTCHA or reputation-scoring challenge (e.g. reCAPTCHA-style), understanding this raises attacker cost but is not unbreakable (section 7). [f753de594e4]
5. Add adaptive/risk-based MFA triggers: challenge for a second factor when the login comes from an unrecognized device/browser (no recognition cookie), a new IP/location/country, an IP on a known-suspicious-IP list, or when one source attempts many different accounts in a short window (source's worked threshold: ~10 accounts within one minute is treated as clearly non-human). [75c876a254f3]

**C. Implement generic-error and constant-time authentication checks (defend against enumeration and timing side channels).**
1. On login, password-reset, and account-creation endpoints, always return the same generic message/HTTP status regardless of whether the username exists, the password is wrong, or the account is disabled — apply this consistently across all three flow types, not just login. [83bd8b5f52f4]
2. Rewrite any early-return authentication check so that the hash-and-database-lookup work runs unconditionally on every path (whether or not the username exists), branching only at the very end on the combined result — this closes the timing side channel that an early return creates. [d3e7e7ef57e6]
3. If the trade-off of fully generic messaging is judged too costly to user experience for your service, use rate limiting instead/in addition, so an attacker cannot enumerate at scale even if individual responses are more specific.

**D. Implement TOTP as a second factor (example flow, contrasted explicitly with SMS).**
1. Server generates a cryptographically random secret key unique to the user and stores it against their account.
2. Present the secret to the user as a QR code (and/or a manually-typeable string) for their authenticator app (example named: Google Authenticator) to scan and store.
3. To generate a code, the app divides the current time by a 30-second interval to get a counter, runs the counter plus the shared secret through an HMAC function, and truncates/reduces the result modulo 10^6 to produce a rotating 6-digit code — this works fully offline since both sides derive the counter from wall-clock time, needing no network round trip.
4. On login, the server independently performs the same time-window + HMAC + truncation steps with its stored copy of the secret and compares to the user-submitted code; a match proves possession of the registered device. [1ce56e83712a]

**E. Implement stateless CSRF tokens (pre-SameSite-cookie-era pattern, still relevant for legacy-browser support and existing codebases).**
1. On serving a form/page that will later submit a state-changing request, compute a token via HMAC over the user's existing session ID plus a server-only secret (avoids having to store/remember every issued token).
2. Embed the token as a hidden form field (`<input type="hidden" name="csrf_token" value="...">`).
3. On receiving the state-changing (POST/etc.) request, recompute the expected token from the request's session ID and the server secret, and reject the request if the submitted token is missing or does not match.
4. Prefer SameSite=Lax cookies as the primary defense where legacy-browser support allows; keep CSRF tokens as a secondary/legacy layer rather than removing them outright if any users are on old browsers or the app is enterprise-facing. [dd0c8d03e16c] [c2bad816cf64] [0d2a5b6f2851]

**F. Method-safe routing to prevent the HEAD-request CSRF bypass class of bug.**
1. Do not implement one handler function that internally branches on request method with a two-way `if request.get? ... else (assume POST)`. Instead register separate handler functions/routes per method explicitly (GET vs. POST as distinct registrations), or add an explicit `elsif request.post? ... else raise` branch that throws/crashes on any unexpected method (including HEAD). [bc21e3deb98d] [9b062a4c9cbf]
2. Do not rely on a framework's implicit "runs before the controller" CSRF-check hook without confirming exactly which methods trigger it; verify it covers every method your controller code assumes has already been checked.
3. If using a framework/router (e.g. Express) that requires per-method handler registration (`app.get(...)`, `app.post(...)`), avoid the catch-all `app.use(...)` pattern for security-sensitive endpoints unless you explicitly handle every possible method inside it yourself.

**G. Node.js project's own coordinated-disclosure pipeline (given as a concrete, real-world worked example of a vulnerability-response process; adapt scaled down for a smaller team).**
1. Reporter submits via HackerOne with a self-assessed CVSS score and CWE classification.
2. HackerOne's own pre-triage layer filters out clearly-invalid reports before they reach the project's security team.
3. Team communicates with the reporter (target cadence: first response within ~24 hours, update within ~48 hours; escalate to every 24-48 hours for high-severity issues) and confirms or closes the report as not-a-bug.
4. Confirmed vulnerabilities are embargoed: nobody with access — including team members' own employers — may disclose before public release.
5. A fix is developed; if the fix is breaking, it may still ship as a minor/patch release under the project's stated security-override policy (principle 19).
6. Before testing a security fix across the full build/CI matrix, lock down CI access to only the security-triage and release teams, to prevent outside observers inferring which zero-day is being patched from build activity/commit names.
7. On release: assign or confirm a CVE, publish the CVSS score, publish a blog post, and post to a public disclosure list/group. [085d0d5d996b] [20e8867f0d35]

## 4. Rules, thresholds and numbers

| Rule | Number / threshold | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Minimum password length | 8 characters (called "bare minimum," still low) | Any password-based login | Current best-practice guidance relayed by lecturer, no single named standard body cited for this exact figure | [81c60e09127f] |
| Maximum password length to allow | Up to 64 characters | Balance usability vs. password-hashing DoS risk | Lecturer's stated best practice | [81c60e09127f] |
| bcrypt input truncation | 72 ASCII characters | Any bcrypt-hashed password longer or with multi-byte Unicode/emoji | Documented bcrypt library behavior | [9d8f903b4f27] |
| Password crack-time cliff | Passwords under ~12 characters (upper/lower/number, no symbols) are crackable if someone really wants to | General password-length guidance | Lecturer's cited chart, exact source not named in transcript | [813fb79b2bef] `[web check]` |
| SHA-256 cracking cost (Microsoft-cited) | ~100 billion hashes/second for ~$20,000 | As of ~July 2019 | Microsoft blog post/paper relayed secondhand by lecturer | [813fb79b2bef] `[web check: figure and date]` |
| Share of real passwords crackable from breach corpora alone | ~70% (up to ~75% adding song lyrics/news headlines) | Attacker starts from real breached-plaintext lists, not blind brute force | Same Microsoft source, secondhand | `[web check]` |
| MFA compromise-reduction claim | ~99.9% less likely to be compromised | Cited Microsoft claim relayed by lecturer | Secondhand, unverified in transcript | `[web check: 99.9% figure]` |
| Early text-CAPTCHA break rates | 92% (EZ-Gimpy) and 33% (Gimpy) | 2003 academic paper on specific early CAPTCHA implementations | Named 2003 paper, not otherwise cited | [115d25c9c19d] `[web check: paper name/authors]` |
| "Broken" threshold used by CAPTCHA researchers | ~1% breakage rate | General CAPTCHA-strength research convention cited by lecturer | Lecturer's stated field convention | [115d25c9c19d] |
| Text-CAPTCHA break rates (2014 ML-based attack) | Yahoo 5%, old reCAPTCHA 33%, CNN 51% | 2014 Stanford-linked research paper | Cited by lecturer, exact paper name not given in transcript | [115d25c9c19d] `[web check]` |
| CAPTCHA-solving black-market price (illustrative, dated) | ~$0.50 per 1,000 solves | As observed by lecturer at time of talk | Anecdotal, no source named | `[web check: current pricing, likely stale]` |
| TOTP code rotation window | 30 seconds | Standard TOTP implementation | Standard mechanism, not source-specific | [1ce56e83712a] |
| TOTP code length | 6 digits | Standard TOTP implementation | Standard mechanism, not source-specific | [1ce56e83712a] |
| Salt size (illustrative) | 16 or 32 bytes | General salting guidance | Lecturer's stated typical range | [9d8f903b4f27] |
| GitHub OAuth bug: response time | Acknowledged in ~8 minutes, fixed in ~3 hours | One specific, dated 2019 HackerOne report | Lecturer's own account of a real, recent report | [21e9f01540df] `[web check: exact date/researcher]` |
| Node.js HackerOne SLA (as of talk) | First response ~24h, update ~48h, met ~92% of the time over a trailing 90-day window (~12 reports in that window, team under ~20 volunteers) | Node.js project specifically, point-in-time | Speaker's own stated operational metrics | [085d0d5d996b] `[web check: stale, point-in-time]` |
| Node.js LTS support window | 3 years | Even-numbered Node.js major release lines | Node.js project's own stated policy | [e19ee93824c2] |
| Node.js major release cadence | Every 6 months | Node.js project's own release policy | Project's own stated policy | [e19ee93824c2] |
| Ecosystem HackerOne disclosed vulnerabilities (at time of talk) | 180+ | Node.js ecosystem-wide HackerOne program, point-in-time | Speaker's own live count | `[web check: stale]` |
| ascii-art npm package CVE severity | CVSS 8.6 | A specific command-injection CVE the speaker walked through live | Real CVE cited by speaker, not independently re-verified here | [0ef686a163b4] `[web check: exact CVE ID]` |
| event-stream attack activation threshold | ~$20,000 wallet balance (reported) | The one specific worked supply-chain attack case | Speaker's own account, not independently verified | [f5ed3504c3e1] `[web check]` |

## 5. Diagnostics and checks

| What to check | How | Good | Bad | Fix / next step | Source basis |
|---|---|---|---|---|---|
| Is a password ever logged in plaintext? | Grep application/HTTP request logs for POST bodies on login/register/reset endpoints | Credentials scrubbed before logging | Raw password visible in any log file any engineer can read | Redact/strip credential fields before logging; treat as an urgent fix (cites Facebook/Twitter incidents) `[web check: incident details]` |
| Does the login endpoint respond identically for "no such user" vs. "wrong password"? | Manually test both cases; compare message text, HTTP status code, and response time | Identical message, status, and near-identical timing | Any of the three differs | Return one generic message/status; equalize work on both code paths (procedure C) [83bd8b5f52f4] [d3e7e7ef57e6] |
| Does the password field accept long, Unicode/emoji input without silent truncation? | Register with a 100+ character or emoji-containing password, then log in with the same string | Full string round-trips and authenticates | Silent truncation or failure to authenticate on long/Unicode input | Pre-hash before bcrypt, or switch to a hasher without the 72-byte cap (procedure A step 3) [9d8f903b4f27] |
| Are authentication attempts rate-limited? | Script or manually send repeated failed logins for one username and from one IP | Requests slow down or get rejected after a threshold | Unlimited rapid attempts succeed with no throttling | Add rate-limiting middleware scoped to username and IP (procedure B) [a84a0c3caf46] |
| Is a sensitive account action (change email/password, add payment method, add SSH key/API key) protected by step-up re-authentication? | Attempt the sensitive action mid-session without re-entering credentials | Re-prompted for password/second factor before the action completes | Action succeeds silently with only the ambient session | Add a "sudo mode"-style re-auth gate before sensitive actions [930806e85a10] |
| Does any HTTP HEAD request reach a controller that assumes only GET or POST? | Send a HEAD request to every state-changing/authorization endpoint and observe whether it falls into POST-handling logic | HEAD is either rejected, or handled identically and harmlessly to GET | HEAD triggers POST-only logic (e.g. skips or bypasses a CSRF check) | Add explicit method whitelisting with a fail-loud `else` (procedure F) [83318b4ce2d8] [21e9f01540df] |
| Are cookies set with SameSite, and which mode? | Inspect Set-Cookie headers on session cookies | SameSite=Lax (or Strict where no cross-site login flow is needed) present | No SameSite attribute, or Strict on a cookie needed for cross-site OAuth login | Add SameSite=Lax; verify legitimate cross-site login flows still work (procedure E/F) [0d2a5b6f2851] [c2bad816cf64] |
| Does `npm install` (or equivalent) run with network access to arbitrary domains? | Inspect the sandbox/container network policy used for dependency installs | Install step is network-restricted to an allowlist, or fully sandboxed/disposable | Install runs unsandboxed on a persistent host with unrestricted egress | Move installs into an ephemeral, network-restricted build step (principle 20/21) [6ada3852334a] [f5ed3504c3e1] |
| Are newly registered passwords checked against known-breach data at signup? | Attempt to register with a password known to be in a public breach list | Registration blocked or flagged | Registration succeeds silently | Integrate an HIBP-style breach-check call before accepting the password [e67276b1419] [d6e5ce45fe0] |

## 6. Tools, settings and named features

- **bcrypt** — password-hashing library; auto-generates and embeds a salt, adjustable work-factor ("rounds"), 72-ASCII-character input cap. Attributed to Niels Provos and David Mazières. `[web check: exact origin year/spelling]` [9d8f903b4f27]
- **Have I Been Pwned (haveibeenpwned.com)** — free breach-lookup service by email; supports email-address alerts and can be queried by a site to check whether a candidate password appears in known breach data before allowing it. [e67276b1419] `[web check: current API terms]`
- **Express Rate Limit** — named Node.js/Express middleware package for rate-limiting authentication routes by username/IP. [a84a0c3caf46] `[web check: current package name/maintenance status]`
- **Google Authenticator** — example TOTP authenticator app used in the worked TOTP flow. [1ce56e83712a]
- **CAPTCHA / reCAPTCHA** — human/bot-differentiation challenge; evolved from text-distortion CAPTCHAs (broken by 2003 and 2014 research) to behavioral/reputation scoring (mouse movement, IP reputation, cross-site trust) to a UI-less background scoring mode. Known weaknesses: relay/farming attacks, paid solving services, and penalizing privacy-conscious users (e.g. Tor Browser users get challenged more due to poor IP reputation). [115d25c9c19d] [00647bf08fc4] [b6026850aadf] `[web check: current reCAPTCHA generation/behavior]`
- **WebAuthn / FIDO2 / CTAP2** — browser API (`navigator.credentials.create()`/`.get()`) plus device-communication protocol for public-key-based authentication; superset of the older U2F/CTAP1. Configuration options named: resident key (credential lives only on the physical/platform authenticator, enabling passwordless/usernameless login), user presence vs. full user verification (biometric/PIN), platform vs. roaming authenticator preference. [cb2bba93c89d] [aa2e164554b4] `[web check: current spec/browser support state, this talk is from ~2019]`
- **YubiKey** — named hardware security-key vendor referenced as an example "something you have" WebAuthn authenticator; some models support USB-C and Lightning for cross-device use. `[web check: current product line/claims]`
- **MITRE / CWE / CVE / CNA** — MITRE runs the CWE (weakness-type taxonomy) and CVE (specific-instance) databases; a CNA (CVE Numbering Authority) can assign CVE numbers directly. Node.js became its own CNA in 2017 specifically to avoid disclosure delays waiting on MITRE. [0ef686a163b4] [e19ee93824c2] `[web check: current CWE/CVE database state]`
- **CVSS calculator** — online tool for scoring a vulnerability's severity across attack vector, complexity, privileges, user interaction, scope, and confidentiality/integrity/availability impact. [0ef686a163b4] `[web check: current CVSS version, e.g. 3.1/4.0]`
- **HackerOne** — vulnerability-disclosure/bug-bounty management platform; provides per-project landing pages, pre-triage filtering, response-time SLA tracking, and a reporter reputation score (illustrative figures cited: roughly -5 for an invalid report, +7 for a confirmed one). [085d0d5d996b] [20e8867f0d35] `[web check: current scoring mechanics]`
- **Internet Bug Bounty (IBB)** — a HackerOne-administered fund paying bounties for vulnerabilities in projects considered "core internet infrastructure" (named participants: OpenSSL, Nginx, Apache, Perl, PHP, Node.js), scoped primarily to remote-code-execution findings. `[web check: current participant list/status]`
- **npm audit** — named tool to check installed package versions against known-vulnerability data. [6ada3852334a] `[web check: current tool behavior]`
- **Greenkeeper / Dependabot** — named automated dependency-update/security-alert tools; Dependabot was noted as recently acquired by GitHub at time of talk. `[web check: Dependabot is now a native GitHub feature; Greenkeeper's current status should be re-verified]`
- **Node.js Inspector / `--inspect` debug port** — Node's remote-debugging protocol; historically vulnerable to DNS-rebinding-based remote code execution when exposed beyond localhost. [d730c5ae8ab2] `[web check: confirm current default port and binding behavior]`

## 7. Examples and case results

- **Facebook/Twitter plaintext password logging** (example, unverified in this transcript): the source states plainly-worded logging code inadvertently captured user passwords in internal logs for years at both companies, viewable by any engineer with routine log access. `[web check: verify incident details/dates before citing]`
- **A Pastebin-style breach-sale listing** (illustrative anecdote, explicitly unverified): the lecturer describes finding, via a short web search, a listing offering a claimed ~32-million-account Twitter database dump for "half a Bitcoin" — presented only to illustrate that plaintext credential dumps get resold cheaply, not as a documented, attributable incident.
- **Security-image/anti-phishing study**: a cited study found 72% of participants still entered their password even when the personalized security image and caption were removed entirely, illustrating that this "factor" provides essentially no real protection. `[web check: study name/year not given in transcript]`
- **GitHub OAuth account-takeover via HTTP HEAD bypass** (real, dated case, most fully documented example in this part): a security researcher obtained GitHub's Rails source (via a legitimate Enterprise trial), found that the OAuth-authorize controller's `if request.get? ... else` branch, combined with Rails' automatic HEAD-to-GET routing and its POST-only CSRF-check hook, let a single unauthenticated HTTP HEAD request (carrying only the victim's ambient session cookie, no CSRF token) grant a chosen app full account authorization with zero user interaction beyond visiting the attacker's page. Result: full account compromise (all private repos; for Enterprise, internal company secrets); described as GitHub's highest bug-bounty payout at the time, affecting Enterprise deployments too. Reported via HackerOne, acknowledged in ~8 minutes, fixed in ~3 hours. [21e9f01540df] `[web check: exact researcher, date, and confirmed bounty figure — not independently verified in this transcript]`
- **Node.js zlib `windowBits=8` DoS (CVE-2017-14919)**: a zlib 1.2.9 security update made `windowBits=8` an invalid raw-deflate parameter, causing an uncaught exception/crash in any Node app whose code path let external input set that parameter; fixed by coercing 8 to 9 in Node's zlib bindings on April 4, 2017 (Node 4.8.2, 6.10.2). [0ef686a163b4] `[web check: confirm CVE details]`
- **Node.js Inspector DNS-rebinding RCE (CVE-2018-7160)**: a malicious webpage open in the same or a network-adjacent browser could use DNS rebinding to reach a locally-bound Node.js debugger/inspector port and gain full remote code execution; fixed by restricting the inspector to localhost by default, shipped as a breaking change under a semver-minor security release. [d730c5ae8ab2] `[web check: confirm CVE details]`
- **`event-stream` npm supply-chain attack** (Bitcoin-wallet targeting): a compromised/malicious publish to the popular `event-stream` package embedded an obfuscated payload, present only in the published npm tarball (not the GitHub source), that activated only when installed at the exact dependency-tree depth of one specific targeted crypto-wallet package, exfiltrating wallet keys once a reported ~$20,000 balance threshold was met; caught before wide production impact due to an unrelated coding mistake by the attacker. [f5ed3504c3e1] `[web check: confirm package name, year, and exact figures]`
- **`registry.nodejs.org` subdomain takeover**: a researcher found an abandoned CNAME record pointing the Node.js project's own registry subdomain at a CDN that didn't require proof of ownership, allowing an effective takeover; reported in good faith and fixed via CNAME deletion and a full DNS audit. [a1984ffa45bb]

## 8. Mistakes the source warns about

- Storing usernames case-sensitively without enforcing uniqueness case-insensitively. [9b569cd2522a]
- Forcing password rotation and composition-complexity rules instead of length + breach-checking. [81c60e09127f]
- Capping or silently truncating password length (legacy-system or bcrypt-truncation causes). [9d8f903b4f27]
- Disabling paste into password fields (breaks password managers, stops nothing real).
- Weak password-hint questions with a small answer space (e.g. an 8-option dropdown hint).
- On-screen mouse-click "secure keyboards" meant to defeat keyloggers (defeated trivially by screen capture).
- Trusting anti-phishing security images/knowledge-based questions as real factors. [b6d76d1c801a]
- Logging passwords in plaintext via naive "log every request" code. `[web check: Facebook/Twitter incident]`
- Returning different error messages, status codes, or response times for "user doesn't exist" vs. "wrong password" across login, reset, and signup flows. [83bd8b5f52f4]
- Relying on SMS or push-notification codes as a strong factor without acknowledging their phishing/relay and (for SMS) carrier-takeover exposure. [9e5baf9f66b1] [b7540e558ff6]
- Deploying strong hardware-key-only authentication without first designing account recovery, risking permanent lockout at scale. [822b4433112b]
- Writing a two-way `if request.get? ... else` (assumed POST) instead of explicitly checking and rejecting unexpected HTTP methods — the direct root cause of the GitHub OAuth bug. [21e9f01540df] [0fd2f1e28cc1]
- Relying on a framework's implicit, method-scoped CSRF-check hook without verifying which methods it actually covers.
- Running `npm install` (or equivalent) directly, unsandboxed, on a persistent production host rather than inside a disposable, network-restricted build step. [6ada3852334a]
- Reviewing only a package's public GitHub source and assuming the published registry artifact is identical. [f5ed3504c3e1]
- Building an overly strict internal security/compliance process that developers route around, and treating that as a security win rather than the "highest vulnerability" it actually is.
- Exposing a Node.js Inspector/debug port on anything but localhost, or without credential protection. [d730c5ae8ab2]

## 9. Caveats, conflicts and what is missing

- Several figures are given secondhand, without a directly citable primary source in this transcript: the Microsoft $20,000/100-billion-hashes-per-second claim and the 70%/99.9% figures attributed to Microsoft; the 2003 and 2014 CAPTCHA-breaking papers (named only vaguely); the Facebook/Twitter plaintext-logging claim; the Pastebin Twitter-dump anecdote (explicitly flagged by the lecturer himself as something he found via a quick search, not a verified incident); the event-stream attack's exact package name, year, and dollar threshold. All are tagged `[web check]` above and should not be repeated as verified fact without independent confirmation.
- This part is a ~2019 recording. WebAuthn/FIDO2 browser support, reCAPTCHA's exact current behavior, Node.js's current LTS lines and release cadence, Dependabot's ownership, and any named vendor's current claims have all likely changed since; every such item is tagged `[web check]` in the sections above rather than repeated as current.
- The source does not give a concrete, ready-to-run threat-modeling template of its own; it points to an external, named-but-not-included document (an internal Google "node-sec roadmap" authored by Mike Samuel) as a recommended starting point, without reproducing its content — treat any team's threat model as needing its own construction, not a drop-in from this source.
- No card in the reviewed range corresponds to two specific worked details from this part: the Internet Bug Bounty program itself (participants, scope) and Node.js's own CI/build-lockdown practice during embargoed security testing, and the serverless/FaaS cost-exhaustion-attack threat model — these are documented above in principles/procedures/tools but have no matching card id to cite; treat them as source-only detail until a card is created or a merge finds coverage elsewhere in this source's other parts.
- The source itself flags several of its own points as open, unsettled industry problems rather than solved rules: WebAuthn's user-facing terminology/UX ("what do we even call this button"), the trade-off between recovery flexibility and takeover resistance, and whether bug-bounty programs create healthy or perverse incentives for an under-resourced team — these are presented in the source as live debates, not settled guidance, and should not be flattened into a single "best practice" in the merged folder playbook.
- No direct conflict between named sources appears within this part; the two guest lecturers and the main lecturer are consistent with each other (e.g. the WebAuthn speaker independently confirms the main lecturer's verdict on anti-phishing security images).

## 10. Card index (cited in this part)

- de68d498e431 — Keep authentication, authorization, encryption, hashing and signing distinct in store design
- d63cc78167711 — Authentication vs Authorization: Keep Session Tokens Out of the Permission Business
- 9b569cd2522a — Username Handling Rules: Case-Insensitive Uniqueness, Preserved Display Case
- 81c60e09127fe — Modern Password Policy: Length Over Complexity, Breach-List Checks, No Forced Rotation
- 656bf5b54a5b0 — Password Handling Mistakes That Break Security and Usability
- f753de594e4c8 — Defending Against Network-Based Guessing: Rate Limiting, Lockouts, CAPTCHA
- 115d25c9c19dd — CAPTCHA Limits: Why Human Checks Alone Won't Stop Bots
- 813fb79b2bef6 — Offline Cracking Realities Shape Password-Length Guidance
- a55298b2b4011 — Multi-Factor Authentication: Knows, Has, Is — and Why Biometrics Stay on Device
- b6d76d1c801a7 — Fake Security Indicators: Anti-Phishing Images and Positive UI Cues Don't Work
- 7234ed15210a1 — Security-vs-Usability Tradeoffs: Match Friction to the Value at Risk
- 103d992322b16 — Defense-in-Depth: Assume the Password Is Already Compromised
- b6026850aadf2 — CAPTCHA strength is weaker than it looks — treat it as a speed bump
- 00647bf08fc47 — Reputation scoring and invisible challenges (modern reCAPTCHA-style)
- 930806e85a105 — Step-up re-authentication for sensitive ecommerce actions (sudo mode)
- 83bd8b5f52f41 — Generic error messages to stop account enumeration on login, signup, and reset
- d3e7e7ef57e6b — Avoid timing side channels in authentication code paths
- a84a0c3caf468 — Rate limiting authentication attempts — and the shared-IP caveat
- e67276b14195 — Check signup passwords against breach lists (Have I Been Pwned)
- fe3628d7cc656 — Proactively lock or flag accounts after a breach you're tangentially involved with
- 9d8f903b4f271 — Store passwords with a maintained adaptive password hasher
- 5d7219b293c0c — Store passwords with a maintained adaptive password hasher (duplicate card id elsewhere in source)
- 385b678a734e0 — Why strong passwords alone fail — and what they actually protect
- 75c876a254f30 — Use risk-based step-up checks without weakening admin authentication
- 1ce56e83712a2 — TOTP: implementing a two-factor second factor without SMS
- cb2bba93c89db — WebAuthn and passkeys: replacing passwords with device-based authentication
- c7048790c8bc9 — Use modern, non-guessable factors instead of knowledge-based questions
- a92370ed045d7 — Prevent data-breach exposure from common cloud misconfigurations
- d6e5ce45fe0b0 — Audit your authentication implementation with HIBP and breach-awareness
- 8a2882319f8c9 — Model login security as credential-to-account binding, not factors
- be571a894d845 — Attack the password-reset link as your weakest login path
- c16584de911d2 — Recognize anti-phishing images as a non-factor
- 9e5baf9f66b1a — Rate SMS and app-based one-time codes by interception and phishing risk
- b7540e558ff6f — Use push-notification login, but read approval prompts carefully
- 822b4433112b0 — Design account recovery before you enforce strong factors
- ef94282cf242f — Adopt hardware-backed sign-in and passwordless flows via the browser credential API
- 2124b9d665e3a — Choose between device-bound and synced credentials for shopkeeper and customer logins
- 54dc85fef2012 — Run authentication as a pluggable abstraction so you can adopt stronger credentials later
- aa2e164554b4d — Check the WebAuthn, CTAP and U2F naming before integrating a device
- 357172b29b2f1 — Handle credential-registration privacy between sites
- 9560f29c325ab — Value QR-code cross-device login honestly
- 1a34783ce4eb4 — Treat client certificates and SSH keys as real factors in recovery
- 83f09dc4ed01a — Separate authentication from authorization in the credential design
- 45ceb9e634a15 — Name the customer-facing credential plainly for storefront login
- e19ee93824c2f — Identify and Prioritize Node.js Core vs Dependency vs App Vulnerabilities
- 0ef686a163b47 — Use CVE, CWE and CVSS as a Shared Vocabulary for Storefront Findings
- a1984ffa45bb7 — Threat-Model Your Whole Domain, Not Just Your Software
- d730c5ae8ab28 — Never Expose Node Inspector/Debug Ports on Storefront Servers
- 20e8867f0d35a — Design an Embargo and Coordinated-Disclosure Process for Security Findings
- 085d0d5d996b7 — Set Explicit Response SLAs for Security Reports
- 9a7ac826028be — CSRF fundamentals: ambient cookie authority and forged state-changing requests
- dd0c8d03e16c2 — Implement stateless CSRF tokens with HMAC over the session ID
- 48d54741b489b — Why the CSRF token defeats a forged request: same-origin policy blocks token theft
- c339e8db6ce98 — Validate the method, not just the token, in redirect/callback handlers
- ee5eb9bb739c3 — Use threat modeling to choose controls, not just to list bugs
- 6ada3852334a2 — npm install runs arbitrary code — isolate builds from production hosts
- 77da8c6db02bf — Keep a live dependency inventory and patch systemically
- f5ed3504c3e10 — Audit your dependency supply chain for typosquatting and unreviewed packages
- 83318b4ce2d8d — Method-specific routes prevent CSRF bypass via HEAD
- 0fd2f1e28cc17 — Fail fast when an assumption is violated
- f8b24497d8ed3 — Fix leaky abstractions that hide security-relevant detail
- 6b8b2285c8ec7 — Avoid APIs with insecure defaults or polymorphic signatures
- 925578938d719 — CSRF defense for storefront authenticated actions
- 21e9f01540df3 — CSRF token bypass via HTTP HEAD and framework magic
- 9b062a4c9cbf9 — Defensively whitelist HTTP methods in store endpoints
- 0d2a5b6f2851e — SameSite strict vs lax: don't break OAuth login on your storefront
- 1b76024d8b1a1 — SameSite Lax versus Strict: Choose by Funnel Impact
- ba7be98c2678f — Leaky abstractions in frameworks cause security bugs
- 76589f025712 — Defensive coding: assert assumptions and fail closed on sensitive actions
- bc21e3deb98d5 — Split storefront routes by HTTP method and purpose
- 43566cfc761f4 — Governing agent and integration access with OAuth scopes
- e9b59700a79f4 — Responding to reported vulnerabilities on your store
- ba831619923db — Treat Leaky Abstractions as Likely Edge-Case Holes in Store Code
- 613fd4e14efdf — Use Explicit Code Over Clever Code in Security-Relevant Paths
- 633153c6724de — Fail Early on Unexpected State; Handle Expected Errors Gracefully
- fbdd4166ffd47 — Assume Inputs Are Wrong: Verify Assumptions at the Top of Each Function
- 0021606dab420 — Reject APIs Whose Insecure Path Is the Easy Path
- b7d4c72be09ca — Watch for Hidden Behavioral Switches in Function Signatures
- b8c4d4acd19f7 — Add CSRF Validation Centrally for State-Changing Requests
- f4015dad3b23e — Set Secure, HttpOnly and SameSite on Session Cookies
- 0279d922e722 — Set SameSite on Session Cookies to Stop Ambient Cross-Site Requests
- c2bad816cf647 — Use SameSite cookies to block cross-site state-changing requests
- 05aa24ef18f6e — Ambient Authority via Cookies: Use SameSite
- 638455ba94533 — GET-request and CSRF exposure in storefront logout and account actions

Note: a few card ids above (e.g. the two "Store passwords with a maintained adaptive password hasher" entries at 9d8f903b4f27 and 5d7219b293c0, and the SameSite-cookie family of cards) appear to be near-duplicates within the wider 326-card set for this source. This is left for the pass-2 folder merge to deduplicate, per the template's merge rules; this mini playbook keeps both since it only reports what it found.
