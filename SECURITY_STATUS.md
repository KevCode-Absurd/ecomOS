# Bot and Agent Security: completed

Six documents; 33/33 sections handled, including one excluded editorial header. 412 exported cards for ecommerce storefronts, checkout, account access, integrations and agent permissions.

Coverage: card testing, account takeover, order-risk triage, admin access, session boundaries, XSS/CSRF/SQL injection prevention, dependencies, local integration exposure, prompt injection and scoped agent actions. Classroom attacks were framed as defensive conditions and owned-system validation. Selected browser-engine material was translated into practical operational boundaries rather than instructing a store to implement its own browser.

The extraction prompt now includes a domain-specific defensive scope. Targeted review revised 17 cards, including malware versus transaction-fraud scoring, password rotation/storage, PCI responsibility, dispute thresholds, context-aware rendering, SameSite limits, private-media authorization and speculative agent protocol support. One saved response had null caveats; these were normalized to empty lists without another paid extraction. Raw API results and pre-review cards are retained.

Four security-domain hybrid retrieval checks returned five complete cards each in 1,173-1,600 tokens under the 2,000-token cap. Relevant prompt-injection, fraud, XSS and admin-security guidance surfaced. The prompt-injection results contain overlapping source perspectives, and the compound fraud query includes broader supporting controls. These are relevance/context-size smoke checks, not a security audit, deployed protections or proof of better model outcomes. Historical details remain subject to current implementation checks; the editorial review is targeted, not exhaustive.

Library: 6,595 active cards, all with matching vectors. Keyword and semantic indexes refreshed.

Cumulative settled API estimate: $17.805178. Unresolved reservations: $2.638027. Combined: $20.443205 / $200 overall ($160 working stop). This folder added approximately $0.289 settled usage. These are pipeline estimates, not provider invoices or balances.

Selected reference checks:
- [OWASP prompt-injection prevention](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html): untrusted input and independently constrained tool use.
- [OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html): maintained adaptive hashing rather than raw hashes.
- [OWASP XSS prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html): context-specific rendering and layered defenses.
- [NIST authentication guidance](https://pages.nist.gov/800-63-4/sp800-63b.html): no arbitrary periodic user-password changes.
- [PCI SSC SAQ guidance](https://www.pcisecuritystandards.org/faqs/1443/): confirm the applicable validation route with the acquirer/payment brand.

Cards: data/library-v3/markdown/23-SEC-bot-and-agent-security.md
Checks: data/library-v3/security-retrieval-check.json
Review: data/library-v3/security-review-log.json

All numbered category folders 01-23 are processed. Remaining: 99-multi (81 sections, not started). Local completion only; no GitHub push, hosting or production security controls deployed.
