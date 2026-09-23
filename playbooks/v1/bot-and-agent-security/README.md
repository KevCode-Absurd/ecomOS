# Bot And Agent Security — draft playbook

**Status:** source-linked draft; not owner-approved or outcome-tested.

Read [the operating contract](../OPERATING_CONTRACT.md) before using a workflow.

## Inputs
- Platform
- integrations
- permissions
- payment flow
- logs
- incident scope

## Measures
- Access exposure
- detection/recovery time
- customer impact

## Foundation candidates
Inferred principle labels do not establish universal applicability. Retain source conditions; empty means no matched labelled principle, not absence of foundational knowledge.

- **Assume Breach at the Browser Layer and Design Store Systems for Containment** (`eac31cbbcd3c1f4043c66b00`): Because a browser compromise can read memory and issue commands, design store systems so a single compromised workstation or session cannot reach the whole operation.
  Applies when: Architecting access for ecommerce back office, order management and payment tooling where staff use web browsers all day.
  Condition: This is a defensive inference drawn from the source's browser-attack material rather than a procedure the source itself prescribes; treat it as risk reduction, not a guarantee.
  Condition: Additional factors and least privilege do not stop a compromise of a privileged session that has itself been authenticated.

- **Scope untrusted content and tool output as data, not authority** (`5cbb9c84b9fdf3cb5e76b3f3`): Pages, documents, and agent/tool output can be attacker-influenced and must not be treated as authorization for privileged store actions.
  Applies when: Designing or reviewing ecommerce automation (order bots, support agents, listing tools, integrations) that reads external content or tool output and can take store actions.
  Condition: No single control (HTTPS, hashing, CAPTCHA, WAF, prompt filtering) guarantees security; layer controls and verify against current platform documentation.
  Condition: This card transfers the source's phishing/untrusted-content principle to agent tooling; the source itself did not test agent permission models.

- **Build dedicated agent rails and micro-authorization for verified agents** (`92bf9bab9d443ee24e1ad825`): Rather than heavy-handed WAF rules that block everything, establish isolated pathways and minimal permissions for legitimate AI agents.
  Applies when: Architecting how third-party shopping agents and assistant integrations access your catalog and checkout.
  Condition: Dedicated rails require knowledge of which agents are legitimate; without cryptographic verification or a directory, 'rail' access becomes an open door.
  Condition: The source acknowledges retailers risk disintermediation and reduced customer insight as agents become intermediaries — an architectural trade-off, not only a security one.

## Audit ecommerce integration permissions
Workflow ID: `bot-and-agent-security.access-audit`

**Deliverable:** Access review and remediation plan

### Proposed decision sequence
1. Inventory integrations, owners and data/action scopes
2. Identify unnecessary access and missing separation of duties
3. Propose scoped changes with verification and rollback

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Least-privilege admin access for your store
Card: `a01f3ac62ebb5b6b7adcdd80` · Source: How to Make Your Shopify Store More Secure.docx · Section: 0

Assign each Shopify admin exactly the permissions their role needs, profile it, and revoke unused access immediately.

Applies when: You are adding a team member, agency, or contractor to your Shopify admin and deciding what access to grant.

- Map roles before granting anything: fulfillment staff, content editors, marketing, developer, finance. For each, list the specific admin areas they touch (orders, products, themes, apps, payouts).
- Assign only those permissions. Every additional admin account is a potential risk vector, so treat each grant as a security decision, not a convenience.
- Use time-limited access for temporary contractors — grant for the engagement window and revoke at the end.
- Audit access on a recurring basis (the source suggests regular audits) and immediately revoke permissions that are no longer needed.
- Where the platform supports custom roles, build role-based profiles rather than reusing a broad default.
- Pair with a real-time alert for suspicious admin activity so privilege misuse is visible.
- **Condition:** The source frames least privilege as baseline practice; the exact granularity of Shopify's role options changes over time, so verify the current interface in your admin settings.
- **Condition:** Least privilege is authorization (what a logged-in user can do) and does not replace authentication controls.

#### Build dedicated agent rails and micro-authorization for verified agents
Card: `92bf9bab9d443ee24e1ad825` · Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx · Section: 0

Rather than heavy-handed WAF rules that block everything, establish isolated pathways and minimal permissions for legitimate AI agents.

Applies when: Architecting how third-party shopping agents and assistant integrations access your catalog and checkout.

- Establish dedicated 'agent rails' — isolated, purpose-built pathways for verified agents — instead of opening the same interface to everything or blocking all automation.
- Grant minimal necessary permissions per agent action (micro-authorization), so a hijacked or poisoned agent cannot reach beyond its task.
- Enforce policy-based access controls that distinguish verified agents, humans, and unverified automation, with different rights per class.
- Ensure agent access to user-specific flows is reviewed for data protection implications before enabling it.
- Keep decisions at the edge in real time so policy is applied before traffic touches downstream systems.
- Define and document what each trust tier may do: allow, monitor, rate-limit, authenticate, or block.
- **Condition:** Dedicated rails require knowledge of which agents are legitimate; without cryptographic verification or a directory, 'rail' access becomes an open door.
- **Condition:** The source acknowledges retailers risk disintermediation and reduced customer insight as agents become intermediaries — an architectural trade-off, not only a security one.

#### Assume Breach at the Browser Layer and Design Store Systems for Containment
Card: `eac31cbbcd3c1f4043c66b00` · Source: Site Security (1).docx · Section: 25

Because a browser compromise can read memory and issue commands, design store systems so a single compromised workstation or session cannot reach the whole operation.

Applies when: Architecting access for ecommerce back office, order management and payment tooling where staff use web browsers all day.

- Assume that a machine used for browsing untrusted sites may be fully compromised, and design downstream access accordingly rather than relying on endpoint trust.
- Require re-authentication or a second factor for high-impact actions such as exporting customer records, changing payout or bank details, or bulk-editing prices, so stolen session material alone is insufficient.
- Scope administrative permissions per person and per role, so a compromised session holds only the privileges that operator actually needs.
- Keep high-privilege admin surfaces on separate accounts and separate browser profiles or machines from day-to-day browsing.
- Log privileged actions with actor and source information so anomalous activity from a normally low-traffic workstation can be detected.
- **Condition:** This is a defensive inference drawn from the source's browser-attack material rather than a procedure the source itself prescribes; treat it as risk reduction, not a guarantee.
- **Condition:** Additional factors and least privilege do not stop a compromise of a privileged session that has itself been authenticated.

### Retrieval and applicability
Search: `least privilege access control authentication agent permissions`
Related domains: store-setup, measurement, team-and-management
Mixed-folder candidate IDs: 3097cac99a358c85187e1e13, 99016d30d66e7ea7f808804b, e1abe7ca30f5e8577e6ad432

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

## Review storefront security controls
Workflow ID: `bot-and-agent-security.store-security`

**Deliverable:** Storefront security review

### Proposed decision sequence
1. Map sensitive purchase paths and existing controls
2. Review evidence of exposure without conducting intrusive tests
3. Prioritise protection and recovery checks with responsible owners

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Defend against digital skimming and payment-page tampering
Card: `00fe8dc22000ebe5e90a1b11` · Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx · Section: 0

Card skimming (Magecart-style attacks) injects code into checkout to steal card data; protect by minimizing third-party scripts and monitoring checkout code.

Applies when: Managing checkout page scripts, tags and third-party apps, or investigating an incident where card data may have been captured from your site.

- Inventory every script and app that loads on checkout and payment pages, including analytics, chat, A/B testing and tag managers, and remove anything that does not need to run at the payment step.
- Restrict who can edit checkout templates and scripts, and require review for checkout code changes, since injected skimming code typically arrives through a compromised admin account or third-party dependency.
- Use hosted payment fields or redirect flows so raw card numbers never enter your page's DOM where injected script could read them.
- Monitor checkout code and script sources for unexpected changes, and route alerts to a named owner who can act quickly.
- Include checkout integrity checks in your regular security review, alongside malware scans, so tampering is detected even if the script is served from a legitimate-looking domain.
- If skimming is suspected, treat it as a card-data breach: isolate, rotate credentials, notify your payment provider and follow your incident process.
- **Condition:** The source names Magecart as a category but provides no technical detection recipe; methods vary by platform and should be validated on systems you own.
- **Condition:** No control fully eliminates skimming risk while third-party scripts run on checkout.

#### SSL Certificates: What They Do and Do Not Protect
Card: `c8a995754b003d5ec0933bed` · Source: Ecommerce security — what it means, common threats, and modern best practices.docx · Section: 0

Use SSL certificates to verify site identity and encrypt connections, while recognizing they do not substitute for checkout-specific skimming controls.

Applies when: Establishing or reviewing baseline transport security on a storefront, or explaining to stakeholders what SSL does and does not cover.

- Deploy an SSL (secure sockets layer) certificate, which per the source verifies a website's identity and serves as an encrypted connection.
- Rely on it to protect credit card details and other sensitive transaction data in transit, and to prevent attackers from using your site as part of a phishing attack.
- Treat SSL as one layer rather than the whole program — the source positions it alongside CDNs, firewalls, and antivirus/antimalware as separate best practices.
- Combine with checkout-page controls (patching, ad-code vetting, API updates) because SSL does not stop code injected into the checkout page from capturing data before transmission.
- On hosted platforms, confirm who provisions and renews the certificate under the platform's shared responsibility model.
- **Condition:** The source does not claim SSL alone secures a storefront; treating it as sufficient would leave skimming and account risks unaddressed.
- **Condition:** Certificate provisioning, renewal, and configuration specifics differ by host and change over time — verify against your platform's current documentation.

#### Keep authentication, authorization, encryption, hashing and signing distinct in store design
Card: `de68d498e43178c1ae0baeb2` · Source: Site Security (1).docx · Section: 15

Confusing encryption, hashing, signing and authentication leads to wrong security controls; each addresses a different property and the source's TLS discussion illustrates the distinction.

Applies when: You are specifying security requirements for storefront accounts, payment integrations, agent credentials or admin access and need to state each control precisely.

- Separate the properties: TLS/HTTPS provides confidentiality, integrity and authentication of the server; hashing (like the SHA-256 used for pinned keys) is one-way and verifies material, not identity by itself.
- For server identity, the relevant control is certificate validation against a trusted chain — not the lock icon and not the mere presence of HTTPS.
- For integrity of a DNS-based control such as CAA, note that DNS is not integrity-protected in the source's account, so the control is advisory.
- Apply the same discipline to store accounts and bot defense: do not describe CAPTCHA, a WAF or a prompt filter as guaranteeing security — none of them alone is a guarantee.
- Write requirements as testable statements (which property, which mechanism, which failure mode) so engineering and vendor claims can be checked.
- **Condition:** The source's specifics about SHA-256 pinning and HPKP describe a deprecated mechanism; the general distinction between key pinning and certificate/serial pinning remains valid.
- **Condition:** Current algorithm and protocol guidance changes; verify against current standards before implementing.

### Retrieval and applicability
Search: `payment tampering skimming WAF security TLS`
Related domains: store-setup, measurement, team-and-management
Mixed-folder candidate IDs: 7dc76b3e9b9f9a89991a8482, c780e415d44d2c082be2c7bd, 724b21f679d08b9959c422d5

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

## Plan ecommerce incident triage
Workflow ID: `bot-and-agent-security.incident-triage`

**Deliverable:** Incident triage plan and evidence log

### Proposed decision sequence
1. Establish affected systems, observed impact and evidence
2. Propose containment within authorised boundaries
3. Define recovery validation and customer-impact follow-up

### Supporting knowledge candidates
These cards were ranked locally for this task. They are evidence to assess, not proof that every proposed step is supported. Full steps and conditions are retained below.

#### Prevent data-breach exposure from common cloud misconfigurations
Card: `a92370ed045d706ca33078d4` · Source: Site Security (1).docx · Section: 17

Breaches frequently stem from simple mistakes — publicly readable object storage, SQL injection, command injection, misconfigured servers — so audit these on your own storefront infra.

Applies when: Reviewing your store's storage buckets, servers, and database access for accidental public exposure.

- Treat public object storage as your first check: the source notes a common cause of large breaches is simply leaving an S3-style bucket accessible to anyone — anyone with the URL can download everything.
- Assume that once an attacker reaches one application server, they can pivot to databases and other servers reachable from it, so limit network reachability from app servers to data stores.
- Audit for injection classes named by the source (command injection, SQL injection) as entry points that lead to full data exfiltration.
- Include breach response in your operational plan: assume you will be breached eventually, and design so the blast radius is small and detection is possible.
- Because the source's lesson is 'even many well-known companies get breached', do not treat your own competence or obscurity as a reason to skip the audits.
- **Condition:** This is a general reminder, not a complete audit checklist — many breach causes are out of scope of the source.
- **Condition:** Assume your customers reuse passwords elsewhere, so even a non-financial breach on your store can enable attacks on other services.

#### Use a readiness checklist to expose gaps in agent-visibility and enforcement
Card: `c9c22f8256c751dda7cbfad3` · Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx · Section: 0

A short checklist across visibility, governance, privacy, and fraud surfaces concrete gaps before they become incidents.

Applies when: Running a periodic security review or preparing for an agent-traffic surge such as a product launch.

- Visibility: confirm you can identify which AI agents access the site, which pages/endpoints they visit, and why they visit (indexing, comparing, extracting).
- Governance: confirm you have a documented AI agent access policy, know which actions to allow vs. block, and can technically enforce the policy (block, rate-limit, authenticate).
- Privacy/compliance: confirm the privacy policy addresses agent interactions and that data-protection implications of agent access to user-specific flows are understood.
- Security/fraud: confirm you can detect malicious agent behavior, protect against agent takeover, impersonation, and abuse, and automatically block unwanted or untrusted agents.
- For each unchecked item, assign an owner and a concrete control (endpoint instrumentation, rate-limit rule, authentication requirement).
- Re-run the checklist after any major change in agent traffic or integration.
- **Condition:** The checklist is DataDome's readiness framing as reported in the source; treat unchecked items as prompts to investigate, not as a certified standard.
- **Condition:** Passing every item does not guarantee protection — the checklist covers visibility and policy, not attack efficacy.

#### Defend against digital skimming and payment-page tampering
Card: `00fe8dc22000ebe5e90a1b11` · Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx · Section: 0

Card skimming (Magecart-style attacks) injects code into checkout to steal card data; protect by minimizing third-party scripts and monitoring checkout code.

Applies when: Managing checkout page scripts, tags and third-party apps, or investigating an incident where card data may have been captured from your site.

- Inventory every script and app that loads on checkout and payment pages, including analytics, chat, A/B testing and tag managers, and remove anything that does not need to run at the payment step.
- Restrict who can edit checkout templates and scripts, and require review for checkout code changes, since injected skimming code typically arrives through a compromised admin account or third-party dependency.
- Use hosted payment fields or redirect flows so raw card numbers never enter your page's DOM where injected script could read them.
- Monitor checkout code and script sources for unexpected changes, and route alerts to a named owner who can act quickly.
- Include checkout integrity checks in your regular security review, alongside malware scans, so tampering is detected even if the script is served from a legitimate-looking domain.
- If skimming is suspected, treat it as a card-data breach: isolate, rotate credentials, notify your payment provider and follow your incident process.
- **Condition:** The source names Magecart as a category but provides no technical detection recipe; methods vary by platform and should be validated on systems you own.
- **Condition:** No control fully eliminates skimming risk while third-party scripts run on checkout.

### Retrieval and applicability
Search: `incident response fraud bot attack recovery logs`
Related domains: store-setup, measurement, team-and-management
Mixed-folder candidate IDs: 14dca5a82dc87d4e6246ee57, b00c278eaa05a1643b9e28fc, 10689aea907787489056a591

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
