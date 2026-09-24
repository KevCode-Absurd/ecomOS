# Protecting E-Commerce from Agentic Swarms and AI Bot Attacks: A Comprehensive Security Report

source_id: 1ZlgsvvrHGD1gYsODiLJa1A8eUsyAfTBS  |  folder: 23-SEC-bot-and-agent-security  |  cards: 17  |  words: 4,435  |  type: report (strategic threat-intelligence / defense-framework report; reads as a compiled research brief, not a vendor's own white paper, though several vendors' own products are described inside it)

credibility: The report gives itself the title "A Comprehensive Security Report," dated September 22, 2026, classification "Strategic Threat Intelligence & Defense Framework." It does not name its own author, agency or publisher anywhere in the text. It carries no first-party data or client results of its own. All numbers and claims are attributed to named third parties: Akamai (traffic share, quotes from Akamai's Reuben Koh), Visa's Persistent Threat Research (PERC), Interpol, Signifyd (a cited table source), IEEE and arXiv (attack-pattern research), Princeton University's "Agent Bazaar" research, DataDome (readiness checklist, Priority Protect product), NIST, and OWASP. Several sections describe named vendors' own products in their own terms (Akamai, Darwinium, Kasada, Google Cloud, F5, DataDome, cside, Visa TAP, Skyfire) — these read as vendor marketing/positioning language relayed by the report, not independently verified capability claims, and are tagged `[vendor claim]` below. `[web check: current version/accuracy]` applies broadly since this is a fast-moving vendor and standards landscape.

date signals: Report dated September 22, 2026. Cites "as of December 2025" Akamai traffic-share figure, "early 2026" fraud-pressure and card-testing figures, a "Jan-Apr 2026" card-testing window, and "OWASP Top 10 for Agentic Applications (2026)" released "December 2025." All protocol names (Visa TAP, Mastercard Agent Pay, Skyfire KYA, WBA, UCP, SPIFEE) and vendor product names are current as of that date and should be re-verified before use, since this space is described in the source itself as "still forming."

**Structural note:** the exported text appears to contain two separate write-ups on the same topic stitched together in one file. The first (Executive Summary through Section 8 + Conclusion) is the fuller version with vendor detail, a checklist and a 4-phase roadmap in prose. The second, starting at "Defending E-Commerce Platforms Against Agentic Swarm Attacks / 1. Executive Summary," repeats much of the same material in a shorter form with its own 4-phase roadmap table. This mini playbook treats both as one source and cites card ids as they were assigned, but flags the duplication in section 9.

## 1. What this source is for

Gives a store operator or security lead a framework for deciding how to treat AI agent and bot traffic on an e-commerce site: what distinguishes a scripted bot from an autonomous "agentic swarm," where legacy defenses (WAF, CAPTCHA, honeypots) fail against both legitimate AI shopping agents and malicious swarms, what a layered "trust stack" (cryptographic identity + behavioral monitoring + adaptive response) looks like, which named vendors and protocols currently offer pieces of that stack, and a phased rollout plan from visibility through continuous red-teaming. It is a threat-landscape and architecture briefing, not a step-by-step implementation manual for any single platform.

## 2. Principles

1. **Autonomy is the dividing line between traditional bots and agentic swarms.** Traditional bots execute a predefined task by matching fixed rules and repeat until conditions change; agentic swarms pursue a broader goal, interpret context, weigh options, and adjust tactics based on outcomes, including reportedly shifting user agents, proxies and tactics mid-run when one approach is blocked. Condition: applies when scoping what a bot-management policy needs to detect, not as a claim that every attacker in the wild currently operates this way. [0bb17d46cb5b]

2. **Signal masking cuts both ways.** Legitimate headless AI shopping agents bypass client-side signals (invisible CAPTCHA, honeypot fields, device fingerprinting, UI interaction cues) by design, since they never render a browser UI — this causes false declines under legacy WAF/CAPTCHA rules. Malicious swarms separately evade behavioral biometrics by mimicking human micro-behaviors. Condition: relevant wherever API/headless traffic is currently blocked or challenged by rules built for browser sessions. [4bd8e2130f19]

3. **Identity alone is not enough; pair a credential with behavior.** The source's "Passport/Immigration Officer" model: a cryptographic identity protocol (Visa TAP, Skyfire KYA, WBA) is the passport, proving who the agent is and who it represents; edge behavioral monitoring is the immigration officer, checking whether real-time behavior still matches declared intent. A verified agent from a compromised server should still be blocked; a verified agent that declared "browsing" but starts scraping or testing cards should still be caught by behavior analysis. [fd742c23a1a4]

4. **Scale friction to risk, continuously, not once at entry.** Darwinium's adaptive model (a named vendor framework, `[vendor claim]`, not a standard) scales response in four tiers: permit low-risk browsing/discovery, verify on behavioral shifts, challenge (step-up auth) on financial/account risk, prevent confirmed malicious automation. Sessions should be re-evaluated continuously; if behavior changes after entry, re-challenge or remove the visitor rather than trusting the initial check. Condition: thresholds for what counts as "low risk" vs. "financial risk" are not given in the source and must be set from the store's own baseline data. [020fc68d22aa]

5. **Move stringent verification to transactional points; keep browsing frictionless.** Legitimate agents need broad research access before a transaction. Apply the strictest checks at checkout, account modification and other high-risk actions rather than blocking or heavily challenging the browsing/catalog phase. This is stated as a defense principle in both halves of the source. [8f42796a535c] [020fc68d22aa]

6. **Prefer challenge over block for ambiguous activity.** When suspicious activity is detected, the source's stated preference is a dynamic challenge (e.g., step-up auth, AI-resistant QR flow) rather than an immediate outright block, because block-everything risks losing legitimate agent-driven revenue as well as human customers.

7. **Trust asymmetry, partial context and delegation loops are the core multi-agent failure modes to design against.** Documented patterns (Header Heist, Telephone Loop, from academic research) show: (a) a specialist agent acting on a peer's relayed instruction without verifying the original source (inter-agent trust asymmetry, TV2); (b) context lost across delegation hops so the agent taking the final action doesn't know sensitive data is involved (partial context, TV3); (c) instructions re-summarized at each hop until the executing agent sees only a benign-looking task (telephone-game drift, TV6); (d) malicious behavior split across multiple sites/agents so no single step looks anomalous (distributed attack feasibility, TV4); (e) an induced delegation cycle that exhausts budget and corrupts run state (runaway delegation, TV7). Condition: named patterns come from arXiv/Princeton academic research as reported by the source — illustrative threat models to test against, not confirmed incidents at a named retailer. [fbb1b568c8de]

8. **Any content an agent reads is untrusted data, not instructions.** Product descriptions, reviews, third-party feeds and support messages can carry prompt injection that redirects an agent from the customer's task to an adversary's goal. Enforce action permissions and business rules outside the model even if the prompt or retrieved content is malicious; don't rely on input filtering alone. Corrupted data sources also cause data poisoning that cascades failures across connected agents. [b60907b4beaf]

9. **Grant tools and API access by scope (least privilege / micro-authorization).** An agent that reads catalog data should not also hold payment or admin credentials. Each agent action should be independently authorized against merchant policy rather than inherited from a peer's approval, limiting blast radius if an agent is hijacked or poisoned. [b60907b4beaf] [92bf9bab9d44] [080cf07bec99]

10. **API exposure is a known, largely unmapped gap.** Most commerce respondents (source's cited figure: 85%) had at least one API-related incident in the past year, yet only 22% knew which of their APIs exposed sensitive data. Continuous discovery of documented and undocumented endpoints is the base control. [451e14c2682c]

11. **The "block everything" posture is obsolete; the goal is trust-based, intent-based management.** Merchants face what Akamai's Reuben Koh calls (per the source, `[vendor claim]`/quote) a "split-brain scenario": they can't block all non-human traffic because fewer humans visit directly, but they can't open the floodgates either. The fix is assigning differentiated access by agent identity, behavior and business relationship, with policy set per endpoint and action (browsing vs. checkout vs. account change), not one allow/block switch for the whole site. [85ca7b8e6112]

12. **Off-site third-party shopping agents threaten disintermediation more than on-site ones.** The source reports consumers currently trust a retailer's own on-site agent about three times more than an off-site third-party agent. This is presented as a current, reportedly changeable finding — condition it on `[web check: current consumer trust data]` before betting architecture on it. [85ca7b8e6112]

13. **Model the true cost of fraud, not just direct loss, when building the business case.** The source's total-cost framing: every $1 lost directly to fraud costs roughly $5.13 once chargebacks, operations and product loss are counted. Pair this with the mirror-image loss — revenue lost to false declines of legitimate agents — since that side is easy to overlook and harder to instrument. [b18886d897bc]

## 3. Procedures

The source gives two overlapping phased rollouts (see structural note above). Both are kept here since neither the template nor the source resolves them into one; an implementer should pick one cadence, most likely the 4-phase/week-numbered version since it is more detailed.

**Roadmap A — 4-phase, week-numbered (first half of source):**

1. **Phase 1: Assessment (Weeks 1-4).**
   1. Audit current bot detection and WAF configurations — document what is actually blocked, challenged and allowed today.
   2. Identify all APIs and endpoints exposed to agent traffic, including undocumented ones.
   3. Baseline current AI agent activity: which agents, which pages/endpoints, what intent (indexing, comparing, extracting).
   4. Document existing policies around automated access (many are informal and unwritten). [3d6f02145cdb]

2. **Phase 2: Policy Development (Weeks 3-6).**
   1. Define agent access policies: allow, monitor, rate-limit, authenticate, or block, per category.
   2. Establish trust tiers for different agent categories.
   3. Align privacy policy and terms of service with agent interactions.
   4. Define escalation and human-in-the-loop thresholds for ambiguous or high-risk sessions. [6f8cd064c89c]

3. **Phase 3: Technical Implementation (Weeks 5-12).**
   1. Deploy edge-based behavioral intelligence and anomaly detection.
   2. Integrate cryptographic agent authentication (TAP, KYA, or WBA). `[verify UI: vendor console/config steps]`
   3. Implement adaptive response actions (permit/verify/challenge/prevent).
   4. Establish dedicated agent rails and micro-authorization flows.
   5. Configure AI-resistant challenges (e.g., dynamic QR flows) for high-risk actions. `[verify UI]`

4. **Phase 4: Continuous Operations (ongoing).**
   1. Monitor agent activity dashboards and verification pass/fail rates. `[verify UI: vendor dashboard]`
   2. Tune policies based on observed behavior and emerging threats.
   3. Conduct regular red-team exercises simulating agentic swarm attacks (multi-agent delegation, prompt injection via processed content, scraping, card-testing) — only on systems you own and are authorized to test.
   4. Update defenses as new protocols/standards emerge. [d60649c68a16]

**Roadmap B — 4-phase table (second half of source, overlapping content):**

1. **Visibility:** establish baseline traffic intelligence — map all internal/external APIs and deploy behavioral telemetry to distinguish human, legitimate-AI, and malicious-swarm traffic.
2. **Access Control:** modernize verification points — shift from static CAPTCHAs to dynamic intent-based verification, enforced specifically at checkout and account-modification endpoints.
3. **Hardening:** secure LLM and API infrastructure — enforce strict microsegmentation, sanitize chatbot inputs to prevent "leaky faucet" exploits, block AI token freeloading scripts.
4. **Adaptation:** enable continuous intelligence loops — security decisions should reflect current behavior, not historical classification, adapting in real time to shifting agent tactics.

**Procedure: readiness self-check (DataDome's checklist, `[vendor claim]` origin, as relayed by the source).** Run this before or alongside baselining:
- Visibility & Detection: can you identify which AI agents access the site, which pages/endpoints they visit, and why (indexing, comparing, extracting)?
- Policy & Governance: do you have a documented AI agent access policy, do you know which actions to allow vs. block, can you technically enforce the policy (block, rate-limit, authenticate)?
- Privacy & Compliance: does your privacy policy address AI agent interactions; do you understand data-protection implications of agent access to user-specific flows?
- Security & Fraud: can you detect malicious agent behavior, protect against agent takeover/impersonation/abuse, and automatically block unwanted or untrusted agents?
- For each unchecked box, assign an owner and a concrete control (endpoint instrumentation, rate-limit rule, authentication requirement). Re-run after any major change in agent traffic or integration. [c9c22f8256c7]

## 4. Rules, thresholds and numbers

| Rule / figure | Number | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Share of commerce traffic that is AI bots | 47.9% of all commerce traffic on Akamai's global network | As of December 2025 | Akamai, `[vendor claim]`, `[web check: current figure]` | b18886d897bc |
| AI bot traffic growth | surged 300% over the past year | Trailing 12 months as of report date | Cited by report, unattributed further | (executive summary, no dedicated card) |
| AI bot request volume | >25 billion AI bot requests | Two-month period, commerce industry | Cited by report | (executive summary) |
| AI traffic to US retail sites | +4,700% year over year | Report date context | Cited by report | (executive summary) |
| Profitability of AI-tooling fraud | 4.5x more profitable | Per Interpol | Interpol (cited) | (executive summary) |
| North American fraud pressure | +33% | Early 2026 vs. 2025 | Cited by report | (executive summary) |
| AI-driven card-testing increase | +175% | Jan-Apr 2026 | Cited by report | b18886d897bc |
| Total cost multiplier per $1 lost to fraud | ~$5.13 (chargebacks + ops + product loss) | US retailers, specific measurement period | Cited by report; treat as directional, not your store's economics | b18886d897bc |
| Web attacks targeting APIs | +9% year over year | — | Cited by report | 451e14c2682c |
| Orgs with >=1 API incident in past year | 85% of commerce respondents | — | Cited by report | 451e14c2682c |
| Orgs that know which APIs expose sensitive data | only 22% | — | Cited by report | 451e14c2682c |
| Layer 7 DDoS volume against commerce | ~3 trillion attacks in 2025; retail = 84% of that volume | 2025 | Cited by report | 451e14c2682c |
| Dark web "AI Agent" mentions | +450% over six months | vs. prior six-month period | Visa PERC | (Section 1.3, no dedicated card) |
| Monitored AI bot activity allowed through unrestricted | "three-quarters" (75%) | Due to lack of granular differentiation | Cited by report's sources | 4bd8e2130f19 |
| Consumer trust: on-site vs. off-site agent | ~3x more trust in on-site retailer agents | Reported finding, may change | Cited by report | 85ca7b8e6112 |
| Signal processing volume (DataDome Priority Protect) | 5 trillion signals processed daily | Vendor product claim | DataDome, `[vendor claim]` | (Section 5.1, no dedicated card) |
| Akamai market reach | 9 of top 10 retailers rely on Akamai | Vendor claim | Akamai, `[vendor claim]` | (Section 5.1, no dedicated card) |
| Roadmap A timeline | Weeks 1-4 / 3-6 / 5-12 / ongoing | Planning heuristic, not validated schedule; adjust to scale/risk | Report's own phasing | 3d6f02145cdb |

## 5. Diagnostics and checks

- **False-decline audit:** trace decline reasons on blocked API/headless traffic. Separate "no client-side telemetry" (a channel signal, not intent) from genuine malicious patterns. If declines cluster on headless/API traffic with no other risk signal, the rule is likely misconfigured for signal masking, not catching fraud. [4bd8e2130f19]
- **Intent-drift check:** compare an agent's declared entry intent (browsing vs. paying) against observed actions through the session. Good: actions stay within declared scope. Bad: an agent that entered as "browsing" starts scraping catalog/pricing at volume or testing card numbers — this is intent drift and should trigger verify/challenge/prevent, not be waved through because the credential checked out. [fd742c23a1a4] [8f42796a535c]
- **Cart-reservation-to-conversion check:** track how much reserved/claimed inventory during a drop never converts to a real order. High claim-to-no-conversion ratio signals hoarding bots (Grinch bots) rather than real demand. [8f42796a535c]
- **API sensitive-data inventory:** for every discovered API (including undocumented ones), determine whether it exposes sensitive data. The source's cited baseline is that only 22% of organizations know this — treat "we don't know" as the expected starting state, not a red flag unique to your store, but still a gap to close. [451e14c2682c]
- **Delegation-trust check (for agent-integrated storefronts):** for any action an agent takes because another agent "relayed" an instruction, verify against the original source before allowing it. Bad: a file/data-handling agent acts purely because a peer agent said to. [fbb1b568c8de]
- **Readiness checklist run-through:** work through the four DataDome-framed categories (visibility, governance, privacy/compliance, security/fraud) above; for each unchecked item assign an owner and a concrete control. Re-run after any major change in agent traffic or integration, and periodically for a launch or drop. [c9c22f8256c7]
- **Session re-evaluation check:** confirm the bot-management setup re-evaluates behavior continuously within a session, not just once at entry — a system that only checks identity/behavior at session start will miss intent drift that starts mid-session. [020fc68d22aa]

## 6. Tools, settings and named features

All vendor descriptions below are relayed from the source and are vendor claims about their own products (`[vendor claim]`); verify current capability, pricing and integration requirements before committing architecture. `[web check: current product/version]` applies to this whole section.

- **Visa Trusted Agent Protocol (TAP):** identity/passport layer; cryptographically signs transaction intent; ecosystem framework developed with Cloudflare; supported (per source) by Adyen, Ant International, Checkout.com, Coinbase, CyberSource, Elavon, Fiserv, Microsoft, Nuvei, Shopify, Stripe, Worldpay; available on Visa Developer Center and GitHub. `[verify UI]`
- **Mastercard Agent Pay:** named alongside TAP as a cryptographic identity protocol; no separate configuration detail given in the source.
- **Skyfire Know Your Agent (KYA):** open protocol for agent identity and payment infrastructure; uses standard JWTs compatible with OAuth2, HTTP and JWKS; interpreted at the edge by F5 Distributed Cloud Bot Defense to enforce access policy in real time.
- **Web Bot Authentication (WBA):** IETF standard for HTTP message signatures letting agents cryptographically prove identity; integrates with Google Cloud Fraud Defense per the source.
- **Ant International / Mastercard / Visa KYA Interoperability Framework:** collaboration for shared certification and continuous transaction monitoring, linking each agent to a validated operator/cardholder/organization.
- **Akamai (+ Visa integration):** edge-based behavioral intelligence, user recognition, bot/abuse protection; combined with Visa TAP for real-time insight into agent activity before it reaches sensitive systems. `[vendor claim]`: "nine of the world's top 10 retailers rely on Akamai."
- **Darwinium Agent Intent Intelligence:** deployed natively at the edge on Cloudflare and AWS CloudFront; evaluates each request for origin (verified agent / human / malicious automation); source of the permit/verify/challenge/prevent four-action model; interoperates with Visa TAP, Mastercard Agent Pay, and emerging KYA models.
- **Kasada AI Agent Trust:** verified-bots/agent directory with vendor identity and category data; policy-based access controls; real-time edge enforcement; reporting on verified agent activity.
- **Google Cloud Fraud Defense:** positioned as the "next evolution of reCAPTCHA" for the agentic web; includes an agentic activity measurement dashboard, an agentic policy engine, an AI-resistant QR-code challenge; integrates with Web Bot Auth and SPIFEE.
- **F5 Distributed Cloud Bot Defense (+ Skyfire):** recognizes agents carrying Skyfire KYA tokens; gives visibility into agent identity and the human/enterprise principal behind the request; works within existing stacks with no re-platforming claimed.
- **DataDome Priority Protect:** "virtual waiting room" for agentic commerce; continuous in-session validation; AI-powered request classification (5 trillion signals/day claimed); differentiated access policies for humans/agents/bots; priority lanes for trusted agents.
- **cside AI Agent Detection Toolkit:** detects AI agents operating inside consumer browsers (named examples: Comet, ChatGPT Atlas, Manus) plus cloud-based automation; dynamic page-element changes and step-up verification for higher-risk actions; integrates with VPN detection and geographic traffic analysis. Stated philosophy: "Agents aren't inherently bad, bad actions are bad."
- **Universal Commerce Protocol (UCP):** developed by Google and Shopify for agentic-commerce interoperability.
- **SPIFEE:** industry standard for agentic traffic identification and classification (named alongside Web Bot Auth; likely "SPIFFE" — confirm spelling/identity with `[web check]`).
- **NIST AI Agent Standards Initiative (via CAISI):** supports interoperable/secure AI agent systems; NIST AI Risk Management Framework emphasizes documentation, monitoring, human oversight, context-sensitive controls.
- **OWASP Top 10 for Agentic Applications (2026):** released December 2025 via the OWASP GenAI Security Project; risk categories include prompt injection, unsafe tool use, and supply-chain vulnerabilities in agentic systems, called out as directly relevant to financial services/payments/fintech.

## 7. Examples and case results

- **Header Heist attack (illustrative academic scenario, not a named real breach):** a fabricated "fix" for a legitimate server error, posted on an untrusted forum, is read by one agent in a crew and alters its flow from shopping to uploading session information. The fix spreads from the discovering agent to the rest of the crew via peer delegation, triggering cascading pursuit of the adversary's goal. Exploits inter-agent trust asymmetry (TV2), partial context (TV3), and telephone-game drift (TV6). [fbb1b568c8de]
- **Telephone Loop attack (illustrative academic scenario):** two attacker-controlled sites chain together. A Dispatcher agent routes a task to an "E-Commerce Specialist" agent, which clicks an attacker-placed link to a fake review aggregator. That site's registration form requires a second agent's involvement, which is then instructed to delegate back to the first agent — creating a circular delegation the system cannot resolve, exhausting budget and corrupting run state (runaway delegation, TV7) without reaching the user's goal. [fbb1b568c8de]
- **"The Crash" (Princeton Agent Bazaar research, B2C market simulation):** a state-of-the-art LLM agent can solve complex logic puzzles while simultaneously driving a simulated market into collapse through locally rational but globally destructive pricing decisions, amplifying price volatility until the market fails. Presented as a research finding on emergent economic failure, not an observed live-market event.
- **"The Lemon Market" (Princeton Agent Bazaar research, C2C market simulation):** a single deceptive agent controlling multiple coordinated seller identities (Sybil) floods a marketplace with fraudulent listings, eroding trust and consumer welfare. Models in the study largely failed to self-regulate; failure severity varied by which model was used, not by model size.

## 8. Mistakes the source warns about

- Treating "bot" as one threat class instead of separating legitimate shopping assistants (research/catalog browsing) from malicious automation — they can look similar in raw traffic. [0bb17d46cb5b]
- Relying on client-side-only signals (invisible CAPTCHA, honeypot fields, device fingerprinting) that legitimate headless agents fail by default, causing false declines. [4bd8e2130f19]
- Trusting a cryptographic credential alone without behavioral monitoring — a verified agent from a compromised server, or one that shifts from browsing to scraping/card-testing mid-session, should still be caught. [fd742c23a1a4]
- Letting a downstream agent act on an instruction "because a teammate relayed it," without verifying the original source (the core Header Heist failure). [fbb1b568c8de]
- Judging individual requests in isolation when malicious behavior is deliberately split across multiple sites/agents so no single step looks anomalous. [fbb1b568c8de]
- Granting a conversational or back-end agent broad operational authority such that a successful prompt injection can reach sensitive actions or data. [b60907b4beaf]
- Not knowing which APIs expose sensitive data — the source's cited baseline is that most organizations don't. [451e14c2682c]
- Blocking all scraping/automation traffic uniformly, which also blocks legitimate comparison-shopping agents and costs sales. [8f42796a535c]
- Setting bot policy before establishing a traffic baseline — "policy without baseline data is guesswork." [3d6f02145cdb]
- Writing a policy that cannot be technically enforced (block, rate-limit, authenticate) — "a policy you cannot enforce is documentation, not control." [6f8cd064c89c]
- Treating passing a readiness checklist as proof of protection — it covers visibility and policy, not actual attack efficacy. [c9c22f8256c7]
- Assuming the source's $5.13 fraud-cost multiplier is your store's actual economics rather than a directional, period-specific figure from cited reports. [b18886d897bc]
- Overlooking false-decline revenue loss (from blocking legitimate agents) when building the cost/business case — easier to miss than direct fraud loss. [b18886d897bc]

## 9. Caveats, conflicts and what is missing

- **Duplicated content within one file.** As noted above, the exported source appears to be two separate write-ups on the same subject concatenated together, with two different phased roadmaps (a week-numbered 4-phase plan and a table-based 4-phase plan) that overlap substantially but are not identical in wording or grouping. Neither is marked as superseding the other. Treat Roadmap A (week-numbered) as the primary sequence since it has more operational detail; Roadmap B restates the same shape with different phase names (Visibility / Access Control / Hardening / Adaptation).
- **No named author or publisher.** The report does not state who wrote it or for whom, only citing third-party sources throughout. This limits how much independent authority to assign it versus its cited sources (Akamai, Visa, DataDome, Signifyd, IEEE, arXiv, Princeton, NIST, OWASP, Interpol).
- **Heavy reliance on vendor self-description.** Every named bot-management/identity vendor's capabilities (Akamai, Darwinium, Kasada, Google Cloud, F5, DataDome, cside, Visa, Skyfire, Mastercard) are described in terms that read as vendor marketing, not independent testing. None of the vendor claims in section 6 should be treated as verified without a `[web check]` against current vendor documentation.
- **No thresholds given for "low risk" vs. "financial risk" tiers**, for risk-based MFA triggers, or for how often to re-baseline or red-team. These are left as store-specific decisions per cards 020fc68d22aa, 080cf07bec99, and d60649c68a16.
- **Named attack patterns (Header Heist, Telephone Loop, The Crash, The Lemon Market) are illustrative academic/research scenarios**, not confirmed real-world incidents at any named retailer — explicitly flagged this way in the cards themselves. [fbb1b568c8de]
- **The 47.9% traffic-share, 450% dark-web-mention, and "three-quarters pass unrestricted" figures are single-source, period-specific statistics** relayed from Akamai and Visa PERC; they are not benchmarked against independent measurement and will age quickly given the stated growth rates. `[web check: current bot-traffic share]`
- **Protocol/standard names may drift.** "SPIFEE" as spelled in the source likely refers to "SPIFFE" (a known identity standard) — `[web check: correct name and current spec]` before citing it externally.
- **No conflict with mainstream e-commerce security advice was found** in this source; it extends standard WAF/bot-management thinking (rate limiting, CAPTCHA, MFA, least privilege, microsegmentation) rather than contradicting it. Its main departure from older conventional advice is explicit: it argues that blocking all non-human traffic is "no longer viable," which conflicts with the older default of blanket bot-blocking — the source treats this as an intentional paradigm shift, not an oversight, attributed to Akamai's stated position.
- **No brand-specific data is in this source.** Every diagnostic and rule needs the store's own traffic, API inventory, and fraud-loss data before it can be applied — flagged inline as `[needs brand data: traffic baseline, API inventory, fraud-cost multiplier, MFA/risk thresholds]`.

## 10. Card index

- 0bb17d46cb5b — Distinguish agentic swarms from traditional bots to set detection scope
- 4bd8e2130f19 — Signal masking: don't misread legitimate headless agents as fraud
- fd742c23a1a4 — Passport/immigration model: layer cryptographic identity with behavioral checks
- 020fc68d22aa — Adaptive response: permit, verify, challenge, prevent by risk tier
- 080cf07bec99 — Prevent agent hijacking and account takeover of stored credentials
- fbb1b568c8de — Multi-agent attack patterns: trust asymmetry, context loss, delegation loops
- b60907b4beaf — Treat prompt injection and untrusted content as an authorization problem for storefront agents
- 451e14c2682c — Defend storefront APIs: continuous endpoint discovery and Layer 7 DDoS awareness
- 8f42796a535c — Counter inventory hoarding and price scraping without blocking legitimate agents
- 92bf9bab9d44 — Build dedicated agent rails and micro-authorization for verified agents
- 3d6f02145cdb — Run a visibility-and-baseline phase before changing bot policy
- 6f8cd064c89c — Define a documented AI agent access policy with trust tiers
- 85ca7b8e6112 — Reconcile 'block the bots' thinking with agentic commerce reality
- 8c4deee0d165 — Map identity and authentication protocols before committing to vendors
- c9c22f8256c7 — Use a readiness checklist to expose gaps in agent-visibility and enforcement
- d60649c68a16 — Stand up continuous monitoring and red-teaming after deployment
- b18886d897bc — Model the fraud cost multiplier when justifying bot-defense spend
