## Four pillars of ecommerce security mapped to store controls
Use when: Auditing or planning your store's security program and deciding which controls to add next across PDP, account, checkout and order records.
- Treat Privacy as keeping customer personal and payment data away from unauthorized parties: require encryption in transit and at rest, restrict admin/data access by role, and limit which apps and integrations can read customer records.
- Treat Integrity as ensuring customer-submitted data is not altered in transit or storage: use TLS, validate and re-confirm order, address and payment details server-side, and keep tamper-evident change logs on orders and customer profiles.
- Treat Authentication as proving both buyer and seller are real: require email verification or magic links for accounts, offer PIN or card verification at checkout, and publish verifiable business identity and contact details so buyers can confirm you are genuine.
- Treat Non-repudiation as making transactions undeniable: retain signed order confirmations, timestamped payment authorizations, consent records and email/confirmation logs so a disputed purchase or chargeback can be evidenced by both sides.
- Assign each control to an owner and review the four pillars quarterly, since gaps usually appear at new touchpoints (subscriptions, B2B portals, additional payment methods) rather than at the original checkout.
Caveat: The four-pillar framing is a conceptual model, not a certification. Meeting it does not by itself make you PCI DSS compliant.

Tags: bot-and-agent-security, compliance, authentication, data-protection, checkout, account-security
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Layered defense: block malicious traffic before it reaches origin
Use when: Designing the network and access architecture of a self-hosted or heavily customized storefront that must absorb bots, DDoS and random malicious traffic.
- Put a CDN or edge proxy in front of the origin server so volumetric DDoS traffic and obvious bot floods are absorbed or filtered at the edge; the source notes CDNs use machine learning to block malicious incoming traffic before it reaches your server.
- Layer a Web Application Firewall in front of the application to filter spam, bad bots and common web attack classes such as XSS and SQLi; configure it in front of the store rather than only on the origin host.
- Add multi-factor authentication to admin panels, hosting, payment dashboards and customer accounts that store payment or address data, so a stolen password alone is not sufficient.
- Apply the same layering to non-web surfaces: DNS, email (for staff and customer-facing sending), and any API or integration endpoint that can trigger orders or refunds.
- Monitor edge and WAF logs for attack patterns and adjust rules; treat the first layer as disposable filtering, not as proof the origin is safe.
- Verify each layer actually passes legitimate checkout and login traffic end to end after any rule change, since over-blocking converts directly into lost orders.
Caveat: The source (quoting Roger Grimes, 2018) states most companies using MFA are still hacked, so MFA is a layer, not a guarantee.
Caveat: CDN, WAF and MFA capability and configuration differ by provider; verify current features and defaults in your own platform before relying on them.

Tags: bot-and-agent-security, waf, cdn, ddos, mfa, defense-in-depth
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## SSL/TLS: encrypt data in transit across every hop
Use when: Setting up or auditing transport security for a storefront, checkout, account area or admin interface, especially after migrating hosts or adding a custom domain.
- Install and maintain SSL/TLS certificates for every customer-facing domain and subdomain, including checkout and account pages, so data is encrypted on each hop between the buyer's device and your server.
- Explain the principle to stakeholders: without encryption, any device between sender and server can read passwords, usernames and card numbers, because data passes through multiple computers before reaching the destination.
- Enforce HTTPS across the whole site and redirect or block plain-HTTP requests; a partially secure checkout does not protect the session.
- Automate certificate issuance and renewal, and monitor expiry, so an expired certificate does not silently break checkout.
- Extend the same transport discipline to integrations: webhooks, payment provider callbacks and fulfillment APIs should be encrypted and authenticated as well.
Caveat: HTTPS protects data in transit only; it does not by itself make you PCI compliant, prevent malware, or secure stored card data.
Caveat: Certificate setup and renewal workflows vary by host and platform; verify the current interface, and note that hosted platforms may manage this for you.

Tags: bot-and-agent-security, tls, encryption, checkout, compliance, transport-security
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## PCI DSS scope: who owns what across hosted vs self-hosted
Use when: Deciding your payment integration architecture, evaluating a hosted platform like Shopify, or assessing how much cardholder-data responsibility your team actually carries.
- Accept the baseline rule from the source: PCI DSS applies to all businesses that handle credit card transactions, and it enforces strict protection of credit card data.
- Reduce scope by not storing or transmitting raw card numbers yourself: use your payment provider's hosted fields, redirect or tokenized checkout so card data never touches your servers.
- If self-hosted, map where cardholder data flows through your infrastructure, apply the standard's requirements to that environment, and keep evidence for audits.
- If on a hosted platform, apply the shared responsibility model: the platform secures its own infrastructure, but you still own your admin account security, app/permission choices, refund and order handling, and any custom code or integrations you add.
- Review annually and whenever you add a payment method, market, or integration, because each addition can change your PCI scope.
- Keep card data out of logs, order notes, support tickets and exported CSVs; storing it there re-expands scope unintentionally.
Caveat: This source describes PCI DSS at a high level only; the actual requirements and current version must be checked against the PCI Security Standards Council and your acquirer.
Caveat: Shared responsibility boundaries vary by platform and plan; verify your specific agreement rather than assuming the platform covers everything.

Tags: bot-and-agent-security, compliance, pci-dss, payments, shared-responsibility, checkout
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Protect against counterfeit sites and brand abuse
Use when: Planning brand-protection work for a store selling branded or high-demand physical goods that phishing and counterfeit sites might imitate.
- Monitor for fake versions of your store: the source notes attackers can create counterfeit sites cheaply, harming reputation and valuations, so set up periodic searches, typosquat monitoring and takedown requests for lookalike domains.
- Add QR code authentication to product packaging so customers can verify authenticity from a smartphone, giving buyers an independent way to distinguish genuine goods from counterfeits.
- Watch for malicious alterations to your own site content designed to divert traffic to competitors or damage reputation; use integrity monitoring and a change log on published content.
- Treat customer data theft as a brand event, not only an IT event: notify affected customers, document what was exposed, and prepare a response plan before an incident.
- Keep robust backups with ransomware protection so a worm, virus or defacement can be rolled back quickly and downtime minimized.
Caveat: QR packaging authentication applies to physical products you control; pure-digital or dropshipped catalogs need different verification methods.
Caveat: The source's framing of counterfeit-site risk is qualitative; no specific detection thresholds or measurement methods are provided.

Tags: bot-and-agent-security, brand-protection, data-protection, backups, trust
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Handle the fraud, dispute and delivery moment of uncertainty
Use when: Reviewing checkout, post-purchase communication and dispute handling to reduce buyer uncertainty and the fraud that exploits it.
- Identify the three high-uncertainty moments the source names: payment, dispute resolution and delivery. These are the points where buyers are most exposed to fraudsters.
- At payment, show recognizable payment controls (card verification, secure-payment indicators) and keep the checkout on a trusted, encrypted domain.
- At dispute resolution, give a clear point of contact for problems and a documented process, so customers do not have to rely on unofficial channels where impersonation happens.
- At delivery, provide tracking and a verifiable record of what was ordered and shipped; this also supports non-repudiation if a chargeback is filed later.
- Be explicit about data collection and usage, not just problem-contact transparency. The source notes many businesses disclose contact points but fail to disclose how personal data is collected and used.
Caveat: The source's suggestion to embed third-party reviews for transparency is promotional and outside this section's defensive scope; treat reviews as a separate trust decision.
Caveat: No specific abandonment or fraud-reduction figures are given for these measures.

Tags: bot-and-agent-security, checkout, post-purchase, trust, customer-communication
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Anti-malware scanning and scheduled detection for storefront files
Use when: Operating a self-hosted or plugin-heavy store and needing a routine for detecting malicious code injected into the site.
- Deploy anti-malware software that scans both your web system and supporting devices; the source's requirement is that it renders hidden malware on your website visible and resolvable.
- Enable scheduled scans (daily, weekly, fortnightly or monthly) rather than relying on manual checks, so the routine survives busy periods.
- Turn on file-change notifications so you learn immediately when store files are modified, which is the typical signature of an injection.
- Prioritize known storefront malware families the source names: credit-card skimming scripts, spam injections, pharma-injection pages, pub2srv and malicious redirects.
- After any detection, treat it as a breach until proven otherwise: rotate admin and integration credentials, check for unauthorized admin users or payment-route changes, and review checkout code.
- Keep backups with ransomware protection so a clean restore is possible if cleaning fails.
Caveat: The source promotes specific third-party scanner and firewall products; the durable practice is scheduled scanning, file-change alerts and credential rotation, not any one vendor.
Caveat: Anti-malware does not replace a WAF, access control or transport encryption; it is one layer.

Tags: bot-and-agent-security, malware, monitoring, digital-skimming, backups, incident-response
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Defend against digital skimming and payment-page tampering
Use when: Managing checkout page scripts, tags and third-party apps, or investigating an incident where card data may have been captured from your site.
- Inventory every script and app that loads on checkout and payment pages, including analytics, chat, A/B testing and tag managers, and remove anything that does not need to run at the payment step.
- Restrict who can edit checkout templates and scripts, and require review for checkout code changes, since injected skimming code typically arrives through a compromised admin account or third-party dependency.
- Use hosted payment fields or redirect flows so raw card numbers never enter your page's DOM where injected script could read them.
- Monitor checkout code and script sources for unexpected changes, and route alerts to a named owner who can act quickly.
- Include checkout integrity checks in your regular security review, alongside malware scans, so tampering is detected even if the script is served from a legitimate-looking domain.
- If skimming is suspected, treat it as a card-data breach: isolate, rotate credentials, notify your payment provider and follow your incident process.
Caveat: The source names Magecart as a category but provides no technical detection recipe; methods vary by platform and should be validated on systems you own.
Caveat: No control fully eliminates skimming risk while third-party scripts run on checkout.

Tags: bot-and-agent-security, digital-skimming, checkout, third-party-scripts, incident-response, monitoring
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Bot, spam and OWASP-class application defense with a WAF
Use when: Configuring application-layer protection for a storefront and deciding what the WAF should block versus allow.
- Place a WAF in front of the store application to filter bad bots, spam and the OWASP top 10 threat classes the source names, including cross-site scripting (XSS) and SQL injection (SQLi).
- Verify your platform path: WAF configurations differ for WordPress, Magento, Opencart, Prestashop, Drupal, Joomla and custom PHP sites, so confirm a supported setup rather than assuming one configuration fits.
- Test the WAF against legitimate checkout, login and account flows after any rule change; false positives block real customers and directly cost orders.
- Combine WAF filtering with rate limiting and bot challenges on high-abuse endpoints such as login, account creation, password reset and checkout submission.
- Review WAF logs regularly to tune rules and identify patterns, and keep a documented bypass path for emergencies so a bad rule does not take the store down.
Caveat: The source names the Astra firewall and its feature claims; treat vendor capability lists as claims to verify in your environment, not guarantees.
Caveat: A WAF does not fix vulnerable application code; it filters traffic in front of it.

Tags: bot-and-agent-security, waf, bot-mitigation, owasp, spam, rate-limiting
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Layer passwords, PINs and magic links for buyer authentication
Use when: Designing customer account login, guest checkout verification, or account-recovery flows for the store.
- Require authentication that proves identity for account access, using recognized methods such as client login credentials and card PINs at the point of verification.
- For friction-averse buyers, use email-based magic links or one-time codes so verification does not require remembering a password.
- Apply MFA or step-up verification to sensitive account actions: changing email or shipping address, viewing stored payment data, and issuing refunds or store credit.
- Verify on the seller side too: publish enough business identity and contact information that buyers can confirm the store is genuine.
- Align verification strength with the action: browsing can stay open, but saved-payment access and address changes should require re-verification.
- Watch for account-takeover patterns in support channels, such as sudden email or address changes before an order, and add manual review triggers.
Caveat: The source notes authentication solutions can require expert help if you cannot implement them yourself.
Caveat: Stronger authentication adds checkout friction; the source does not provide a benchmark for how much friction is acceptable.

Tags: bot-and-agent-security, authentication, account-takeover, mfa, customer-accounts, checkout
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Non-repudiation: keep evidence that orders and consents happened
Use when: Setting up order records, consent capture and chargeback evidence for the store, especially for high-value or subscription orders.
- Accept the principle: non-repudiation is a legal and security layer confirming that communication reached the recipient, so a party cannot deny a signature, email or purchase.
- Retain timestamped records of the order confirmation, payment authorization, terms acceptance and delivery confirmation for each transaction.
- Use digital signatures or authenticated confirmations where available, and store them alongside the order record rather than in a separate system that may not be searchable during a dispute.
- Capture marketing and data consent separately from purchase consent, since the source notes businesses often disclose contact points but not how personal data is collected and used.
- Make the evidence retrievable by support staff before a chargeback deadline so disputes can be answered quickly.
- Review retention periods and access controls so the evidence store itself does not become a privacy or breach liability.
Caveat: Non-repudiation is described as a legal principle; specific admissibility of digital records varies by jurisdiction and should be checked with counsel.
Caveat: The source gives no specific retention period or tooling recommendation.

Tags: bot-and-agent-security, non-repudiation, order-records, chargebacks, compliance, consent
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Treat security failures as a survival risk, not an IT line item
Use when: Making the business case for security investment, or deciding how much budget and staffing to allocate to storefront protection.
- Quantify the business exposure in the terms the source uses: losses in finances, market share and reputation, plus the possibility of criminal charges against the company.
- Present the survival framing to decision-makers: the source reports that almost 60% of small ecommerce stores that experience cybercrimes do not survive more than six months.
- Identify the specific loss mechanisms you face: diverted traffic, stolen customer and inventory data, denied service reducing store functionality, and stolen or altered intellectual property.
- Convert the risk into operational requirements: staffing or expert support for security, backups with ransomware protection, and monitoring that runs continuously rather than annually.
- Revisit the assessment when you add markets, payment methods or integrations, since those increase attack surface and change which losses are plausible.
Caveat: The statistics cited (32.4% of attacks, 29% malicious traffic, 85.6% purchase rate, 60% survival) are dated around 2018 and presented loosely; use them as source-stated framing, not current benchmarks.
Caveat: Survival statistics describe a correlation in the cited reporting, not a causal guarantee for any individual store.

Tags: bot-and-agent-security, risk-assessment, business-case, data-protection, downtime
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Harden store networks against worms, Trojans and destructive payloads
Use when: Establishing endpoint and store-adjacent device protection, especially for teams running order management, warehouse or admin workstations.
- Install and maintain anti-virus and anti-malware protection on the devices and systems that touch the store, admin panels and order data; the source lists this as a necessary minimum alongside firewalls and encryption.
- Recognize the delivery vector: the source notes attackers hide Trojans in fake software, so restrict software installation to approved sources for staff who access store systems.
- Plan for the damage types named: hijacked systems, erased data, blocked data access, and the spread of malicious links to clients and other computers on the network.
- Segment admin and operational networks from general browsing where feasible, so a single infected workstation cannot reach store infrastructure.
- Keep an offline or immutable backup with ransomware protection, and test restoration so recovery is a rehearsed process rather than an untested assumption.
- Educate staff who open order emails, supplier files and attachments, since malicious links can be forwarded onward through your network.
Caveat: Anti-virus and firewalls reduce but do not eliminate infection risk; the source presents them as a minimum, not a guarantee.
Caveat: No specific product or detection rate is endorsed here beyond the source's vendor examples.

Tags: bot-and-agent-security, malware, endpoint-security, backups, ransomware, staff-training
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Route traffic through selective-permeability firewalls
Use when: Choosing and configuring firewall or plugin protection for a self-hosted ecommerce site.
- Deploy firewall protection using ecommerce-appropriate software or plugins that bar untrusted networks and regulate both inbound and outbound traffic.
- Configure for selective permeability: the rule is to permit trusted traffic only, rather than blocking individual known-bad sources.
- Verify outbound rules too, since compromised store code often needs an outbound channel to exfiltrate card or customer data.
- Combine the firewall with the WAF and malware scanning layers so network filtering, application filtering and file integrity are covered separately.
- Test the rules against real checkout, login and webhook traffic after changes, and log blocked events for review.
Caveat: The source promotes a specific vendor firewall; vendor feature lists are claims to verify, and results vary by site architecture.
Caveat: A firewall in front of a vulnerable plugin does not fix the underlying vulnerability.

Tags: bot-and-agent-security, firewall, network-security, waf, self-hosted, monitoring
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Automate high-risk order handling on hosted platforms
Use when: Operating on a hosted platform like Shopify and needing a repeatable process for suspicious orders, refunds or account changes.
- Clarify the shared responsibility split: the hosted platform secures its own infrastructure, while you remain responsible for your admin accounts, apps, data access and order-level decisions.
- Define what counts as a high-risk order for your store (for example mismatched billing and shipping, unusually large first orders, or rapid repeat orders from one buyer) and make the criteria explicit rather than leaving it to staff judgment alone.
- Automate the response on hosted platforms using workflow tooling such as Shopify Flow: tag or hold high-risk orders, notify a named reviewer, and release or cancel based on a documented rule.
- Restrict admin permissions so only authorized staff can refund, export customer data or edit payment settings.
- Log every automated and manual risk decision so patterns can be reviewed and rules adjusted over time.
- Re-verify the current interface and available triggers before building workflows, since platform automation features change.
Caveat: The source names Shopify Flow and hosted-platform handling in this section's header, but the body does not detail the workflow configuration; treat platform specifics as needing verification.
Caveat: Automated rules can produce false positives that delay legitimate orders, so include a review path.

Tags: bot-and-agent-security, order-review, automation, shopify, shared-responsibility, fraud
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Map payment-fraud controls: verification checks at checkout
Use when: Choosing and configuring payment verification settings for checkout, or deciding how much friction to add to reduce card-not-present fraud.
- Distinguish the mechanisms rather than treating them as one control: address verification checks the billing address against issuer records, card verification value checks the printed code, and 3D Secure adds an issuer-side buyer authentication step.
- Enable these checks on your payment provider's settings and confirm they apply to the payment methods and regions you sell into.
- Accept that requiring 3D Secure or strict address matching can convert some legitimate buyers away, so weigh fraud reduction against checkout completion for your own catalog and markets.
- Keep these verification steps separate from transport encryption and compliance work; verification is a fraud signal, not a substitute for PCI DSS or TLS.
- Record which checks fired on each order so disputes and rule tuning have evidence.
- Review chargeback and decline patterns periodically and adjust thresholds rather than setting rules once and leaving them.
Caveat: This source's body mentions 3DS, AVS and CVV only in the section header; it gives no configuration detail, so verify current provider options and rules.
Caveat: None of these checks guarantees fraud prevention, and none replaces PCI DSS obligations.

Tags: bot-and-agent-security, payments, fraud, 3d-secure, checkout, chargebacks
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Defend against denial-of-service and keep the store selling
Use when: Preparing for or responding to traffic floods, slow checkout, or downtime during a peak sales period.
- Assume downtime is a revenue event: the source frames denial of service as preventing legitimate users from using the store and causing a reduction in its functioning.
- Absorb volumetric attacks at the edge with a CDN or DDoS-protection layer, so the origin server is not the first thing hit.
- Rate-limit and challenge high-cost endpoints such as search, cart, login and checkout submission, which bots often target to exhaust server capacity.
- Maintain current backups with ransomware protection so a destructive event can be restored quickly and downtime minimized.
- Prepare a response plan with named owners, customer communication templates, and a decision rule for when to enable stricter mitigation that may inconvenience some buyers.
- Review capacity and mitigation settings before major sale events rather than during them.
Caveat: The source describes CDN machine learning as blocking DDoS threats but gives no capacity figures or thresholds.
Caveat: Strict mitigation can block real customers during high traffic; plan the trade-off in advance.

Tags: bot-and-agent-security, ddos, cdn, uptime, peak-season, incident-response
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Integrity: keep customer data unaltered to preserve trust
Use when: Reviewing how order, address and profile data is edited and stored across the store, especially where staff or integrations can modify customer records.
- Adopt the principle: the business uses customer information as provided, without changing anything, and altering any part of the data causes the buyer to lose confidence in the enterprise's security.
- Prevent silent edits: make changes to shipping addresses, order contents and contact details deliberate and logged rather than overwritten by tooling.
- Validate customer-submitted data on receipt and flag discrepancies instead of auto-correcting them without notice.
- Restrict write access so only the roles and integrations that need to change customer records can do so.
- Show customers what was recorded, via order confirmation and account views, so discrepancies surface early rather than at delivery or dispute time.
- Treat unexplained changes in records as a security signal, since unauthorized alteration may indicate compromise rather than a data-entry issue.
Caveat: Integrity in this source is a conceptual principle; it names no specific validation library or logging standard.
Caveat: Some normalization (address formatting, phone formatting) is operationally necessary; the principle is to avoid altering meaning without the customer's knowledge.

Tags: bot-and-agent-security, data-integrity, customer-data, access-control, order-records, trust
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Privacy: prevent unauthorized access to customer data
Use when: Reviewing app permissions, data exports, staff access and vendor sharing for the store's customer database.
- Define the baseline: a breach of confidentiality occurs when sellers let others access customer information, so the standard is that only the chosen seller accesses personal information and account details.
- Audit every app, integration and agency that can read customer records, and remove or scope down access that is not required for its function.
- Apply a minimum protective stack as the source describes: anti-virus, firewall, encryption and other data protection to safeguard credit card and bank details.
- Limit data exports, and avoid keeping card or bank details in spreadsheets, support tickets or marketing tools.
- Document what personal data you collect and how it is used, since the source notes businesses often disclose a problem contact point but not their data collection and usage practices.
- Review access when staff leave or agency relationships end, since retained credentials are a common confidentiality gap.
Caveat: The source gives the privacy principle and a minimum control list, not a full privacy-regulation compliance program; check applicable law separately.
Caveat: Encryption and firewalls reduce exposure but do not guarantee customer data remains private if access is misconfigured.

Tags: bot-and-agent-security, privacy, customer-data, access-control, apps-integrations, compliance
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Run a continuous security review across store surfaces
Use when: Setting a recurring security cadence for the store rather than reacting only after an incident.
- Accept the source's closing posture: don't stop at basic authentication, SSL and MFA, because attackers keep improving, so implement proactive protection across the website continuously.
- Define a recurring review covering the store surfaces named across this section: transport encryption, authentication and MFA, firewall/WAF rules, malware scans, backups, payment verification settings and admin permissions.
- Assign an owner and a schedule for each review item, and record the outcome so gaps are visible between cycles.
- Include ongoing vulnerability monitoring, which the source names as part of the overall ecommerce-security definition alongside encryption, secure payments, PCI DSS compliance and bot protection.
- Re-run the review after significant changes: new market, new payment method, new app, platform migration or staff change.
- Keep an incident response plan ready, and rehearse the steps for notifying customers and payment partners.
Caveat: The source gives no specific review frequency or checklist depth; set a cadence proportionate to order volume and data sensitivity.
Caveat: Vendor product claims in the source are promotional illustrations of the tactics, not endorsements or performance guarantees.

Tags: bot-and-agent-security, security-review, monitoring, incident-response, compliance, process
Source: E-Commerce Security_ Importance, Issues & Protection Measures.docx

---

## Shared responsibility model: what the platform secures vs. what you secure
Use when: Deciding where to invest security effort for a store on a hosted platform (e.g., Shopify) versus a self-hosted cart, and scoping what your team is actually accountable for.
- Map responsibility: the platform secures servers, payment processing, checkout code and software; the merchant secures login credentials, third-party app permissions, sensitive-customer-data handling, and admin access for team members.
- Accept that the platform cannot compensate for weak merchant-side practices — an admin password of 'password123' or a click on a phishing link hands over the store regardless of platform hardening.
- On self-hosted setups, budget for the work the platform would otherwise do: sourcing and renewing SSL/TLS certificates, achieving PCI compliance, patching server software, and configuring firewalls. PCI compliance alone is cited as costing small businesses roughly $1,000–$10,000 per year depending on transaction volume.
- Prioritize merchant-side gaps first: enable 2FA/passkeys on admin accounts, audit app permissions, and stop storing card data in order notes, emails or spreadsheets.
- Recognize that hosted checkout code is not merchant-editable, which the source says significantly reduces Magecart-style skimming exposure versus self-hosted stores where checkout JavaScript can be injected by attackers.
Caveat: Cost figures and platform behaviors are vendor-published and can change; verify current terms with your platform and processor.
Caveat: Hosted platforms reduce skimming exposure but do not eliminate all fraud, ATO or bot risk.

Tags: bot-and-agent-security, platform-security, compliance, account-security, self-hosted, shopify, access-control
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## CNP fraud and card testing: the mechanism to defend against
Use when: Designing checkout fraud controls, selecting a payment processor configuration, or investigating a spike in small declined/approved orders on your store.
- Understand the attack chain: fraudsters obtain card data through breaches, phishing or skimming, then run small transactions to validate the numbers before using them for larger fraud or selling the validated data on dark web markets.
- Treat unusual clusters of small orders — especially from new accounts, mismatched geographies or repeated attempts on the same card range — as a likely card-testing signal rather than organic demand.
- Use CVV checks so an attacker without physical card access has more difficulty completing a transaction, and AVS to check that the billing address matches the issuer's records.
- Note the source's cost framing: each dollar lost to fraud costs store owners an average of about $4.61 once processing fees, lost inventory and operational disruption are counted (source-specific figure, not a benchmark to plan against).
- Configure processor fraud analysis and automated rules rather than reviewing every order manually, because card testing runs at machine speed.
Caveat: Financial figures are published estimates from the source and its cited research, not guarantees for any single store.
Caveat: AVS/CVV alone do not stop all CNP fraud; enablers like tokenization and 3DS work with them.

Tags: bot-and-agent-security, fraud-prevention, card-testing, checkout, payment-security, cvv, avs
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Chargeback thresholds: know your danger zone
Use when: Monitoring order-risk and dispute metrics, setting an internal alert threshold, or deciding when to escalate fraud controls before processor action forces it.
- Obtain current monitoring definitions, thresholds, periods and consequences from the processor or acquirer.
- Calculate the relevant metrics on the correct denominator; different programs can count disputes and transactions differently.
- Set internal alerts early enough to investigate fraud, delivery and customer-service causes.
- Evaluate authentication, review routing and evidence collection while monitoring legitimate-order declines.
- Confirm coverage conditions before relying on any chargeback-protection program.
Caveat: The source's 0.9%, 1% and average loss figures are not universal current thresholds or guarantees.

Tags: bot-and-agent-security, fraud-prevention, chargebacks, measurement, risk-management, payment-security
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Dynamic 3D Secure and the liability shift
Use when: Configuring checkout authentication to reduce fraudulent chargeback exposure without adding friction to every legitimate order.
- Configure the supported 3DS flow according to processor requirements and applicable authentication rules; frictionless and challenge outcomes are not simply low-risk versus high-risk switches.
- When a cardholder completes the 3DS verification step (one-time code or biometric), the source states the responsibility for a fraudulent chargeback moves from the store to the card issuer for authenticated Visa and Mastercard disputes — confirm the exact current liability-shift rules with your processor and card networks.
- Check whether your payment gateway supports 3DS 2.0 authentication when selecting a processor; this is one of the stated security criteria alongside processor-level PCI DSS certification and tokenization.
- Treat 3DS as a liability-shift and verification tool, not as proof that a transaction is legitimate; step-up authentication does not guarantee the buyer is the cardholder.
- Monitor approval rates and false declines after enabling dynamic 3DS so authentication friction does not silently suppress legitimate conversions.
Caveat: The source cites that only 32.4% of store owners implement 3DS; this figure is a snapshot and may change.
Caveat: Liability-shift rules, coverage and eligible transaction types vary by network, region and processor — verify before relying on them.

Tags: bot-and-agent-security, fraud-prevention, 3d-secure, checkout, payment-security, chargebacks, conversion-optimization
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Automated order risk handling with workflow tools
Use when: Setting up order review and capture automation so fraud decisions scale without a human watching every order.
- Confirm your platform's fraud analysis scores each order low, medium or high using signals such as AVS checks, CVV verification, IP data, proxy detection and unusual purchase patterns.
- Build workflows triggered by order-risk events that: auto-capture low-risk orders, add high-risk orders to a manual review queue, send internal notifications for medium-risk orders, and cancel orders matching specific fraud patterns.
- Use pre-built workflow templates from your platform's help center as starting points, then adapt thresholds to your store's order profile and risk tolerance.
- Revisit automation as order volume and fraud patterns change; a rule set tuned for one season can create either false declines or un-reviewed high-risk captures later.
- Keep a human escalation path for medium- and high-risk queues so automated cancellation rules do not silently reject legitimate high-value customers.
Caveat: Fraud scores are model outputs, not verdicts; both false positives and false negatives are possible.
Caveat: Workflow trigger names and template availability change over time — verify against the current platform interface and help documentation.

Tags: bot-and-agent-security, fraud-prevention, automation, shopify-flow, order-management, risk-management
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## AVS, CVV and 3DS: keep the three verification tools distinct
Use when: Configuring fraud-prevention settings or explaining to your team which control addresses which fraud vector at checkout.
- AVS (Address Verification System): checks whether the billing address provided matches the address on file with the card issuer — useful against stolen-card use where the attacker lacks the correct billing address.
- CVV: the three- or four-digit code on the card; requiring it makes stolen card numbers harder to use without physical access, but it is not proof of cardholder identity.
- 3DS: adds a multifactor authentication step (one-time code or biometric) for higher-risk transactions and can shift fraudulent chargeback liability to the issuer when completed.
- Configure AVS and CVV requirements and decide how checkout handles mismatched billing addresses under Shopify Payments fraud-prevention settings (path cited: Settings → Payments → Shopify Payments → Manage → Fraud prevention; verify current navigation).
- Before enabling AVS, note the source's warning that AVS is deactivated by default in Shopify Payments because fraud analysis handles high-risk transactions separately, and that enabling it alongside fraud analysis can raise false declines on legitimate orders — review your order risk reports first.
- Do not treat any single control as sufficient; combine them and monitor outcomes.
Caveat: No single control guarantees a transaction is legitimate; AVS, CVV and 3DS catch different failure modes and can all be defeated or produce false declines.
Caveat: Admin navigation paths and defaults change — verify the current interface.

Tags: bot-and-agent-security, fraud-prevention, avs, cvv, 3d-secure, checkout, payment-security
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Confirm merchant PCI scope with the acquirer and payment setup
Use when: Understanding your compliance obligations as a small store, or checking that store operations do not introduce non-compliant card-data handling.
- Map where payment data is captured, processed and stored, including apps and customer support.
- Ask the acquirer or payment brand which validation route and SAQ eligibility apply to the actual environment.
- Do not infer the required assessment from a universal 20,000-transaction rule.
- Confirm the hosted provider's scope and retain responsibility for merchant accounts, integrations and handling practices outside that scope.
- Keep payment data out of support messages, order notes and spreadsheets; use approved payment collection flows.
Caveat: Platform compliance does not automatically validate every merchant workflow; requirements depend on the actual environment.

Tags: bot-and-agent-security, compliance, pci-dss, payment-security, data-handling, shopify
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Payment gateway selection: what to verify before committing
Use when: Evaluating a new payment gateway or reviewing whether an existing gateway meets your store's security requirements.
- Verify the gateway is PCI DSS-certified at the processor level — certification of your own storefront does not substitute for processor-side compliance.
- Confirm tokenization is supported: card data is replaced with a non-sensitive token so raw card numbers are not retained in your environment.
- Confirm 3DS 2.0 authentication support so you can apply dynamic step-up verification on higher-risk transactions.
- Compare against a built-in option where available: Shopify Payments is described as PCI-compliant by default and includes fraud analysis, 3D Secure and Shopify Protect for eligible stores; third-party gateways can be used but bring their own compliance and security requirements.
- Check certifications directly with the provider before you commit rather than relying on marketing pages, and re-verify periodically since provider terms and certifications change.
Caveat: Vendor feature claims and program eligibility change; verify with the provider and your own processor.
Caveat: Adding a third-party gateway may complicate which party handles compliance and chargeback liability.

Tags: bot-and-agent-security, payment-security, checkout, pci-dss, tokenization, gateway-selection, 3d-secure
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Account takeover, credential stuffing and phishing defenses
Use when: Hardening customer accounts and admin access against takeover, or assessing the retention risk of an account-security incident.
- Recognize the attack chain: large-scale breaches expose username/password pairs, which attackers test automatically across other sites (credential stuffing), or use for targeted phishing that impersonates a trusted source to harvest credentials.
- Require 2FA on all admin accounts, not just payment-related ones — the source notes 2FA is required to use Shopify Payments but should be enabled everywhere; the setup path cited is profile → Manage account → Security → two-step authentication (verify current navigation).
- Add passkeys as an additional authentication layer where supported.
- Train the team on generative-AI-crafted phishing: check suspicious sender domains, verify any request for credential changes or payment redirects through a separate channel, and give staff a reporting route for suspicious emails, voice (vishing) and SMS (smishing).
- Weigh retention impact: the source cites a survey finding that 75% of consumers say they would stop using a site after an account takeover there and 87% would share the experience with others (survey findings, not a guarantee for your store).
Caveat: 2FA, passkeys and training reduce but do not eliminate ATO risk; attackers also target APIs and support channels.
Caveat: Survey percentages are third-party research snapshots, not benchmarks.

Tags: bot-and-agent-security, account-security, account-takeover, phishing, 2fa, passkeys, retention
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Auditing third-party apps and integrations
Use when: Reviewing app permissions before or after installing storefront, marketing, review or fulfillment apps, or cleaning up an accumulated app stack.
- List installed apps and their permissions from the platform admin (the source cites Settings → Apps and sales channels; verify current navigation) and check what each is permitted to access.
- Remove any app no longer in use — an unused integration with order or customer-data permissions is standing risk.
- When selecting new apps, prioritize those with 'Built for Shopify' status and review scores above 3.75; the source states these have been reviewed against Shopify's technical requirements and are maintained to current platform standards.
- Treat installed apps as part of your data-handling surface: an app with broad permissions can undermine your PCI and privacy posture even when your own checkout is clean.
- Re-audit after adding apps with checkout, payment or customer-data access, since permission scope at install time determines what data the app can reach.
Caveat: Review-score and status thresholds are platform-specific heuristics from the source; verify current app-review criteria.
Caveat: Neither a badge nor a score guarantees an app is secure.

Tags: bot-and-agent-security, app-security, access-control, data-handling, shopify, vendor-review
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Digital skimming (Magecart): why hosted checkout reduces exposure
Use when: Deciding between hosted and self-hosted checkout, or assessing skimming risk from custom checkout scripts and third-party front-end code.
- Understand the attack: attackers inject malicious code into the checkout page to capture debit/credit card details as customers enter them; the source describes these as brute-force attacks targeting JavaScript that are hard to spot without regular code audits.
- If you run a hosted platform, note that the source says hosted stores are significantly less exposed because merchants cannot alter the underlying checkout code — a structural control, not a guarantee.
- If you run self-hosted or heavily customized checkout, add regular code audits and review any third-party JavaScript added to payment pages as a standing practice.
- Restrict who can modify checkout templates and injected scripts; every additional script on the payment page is a potential injection point.
- Do not treat HTTPS or a padlock icon as protection against skimming — skimming captures data after it is typed, inside a page that may still be encrypted in transit.
Caveat: Hosted platforms reduce but do not eliminate skimming or supply-chain script risk from installed apps and tags.
Caveat: The source does not prescribe a specific audit frequency; treat regular audits as a principle, not a fixed schedule.

Tags: bot-and-agent-security, magecart, skimming, checkout, code-audit, platform-security
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Bot attacks, API targeting and DDoS: what to watch
Use when: Investigating suspicious traffic patterns, inventory hoarding, fake account signups or site slowdowns that could be bot-driven.
- Treat the API surface as the priority: the source cites a 2025 Imperva report stating 44% of advanced bot traffic targets API endpoints that handle checkout, inventory and customer account data — so review what your APIs expose and who can call them.
- Watch for bot-driven commerce behaviors: card-testing transaction patterns, pricing-data scraping, bulk fake-account creation, and stockpiling of high-demand products before real shoppers can buy.
- For DDoS, recognize the signature as traffic flooding that locks out real customers; the source does not prescribe a specific mitigation stack, so rely on platform-level protections and your provider's DDoS handling.
- Use early bot-detection signal where available: the source cites an example where a platform's Sidekick flagged a major bot attack on Maggy London's storefront before any other monitoring system (a single case example, not a guaranteed detection capability).
- Prioritize protections by business impact — checkout and inventory APIs affect revenue directly; scraping affects pricing strategy.
Caveat: The 44% API-targeting figure is a third-party report snapshot, not a benchmark for your store.
Caveat: The Maggy London detection case is an illustrative example; do not assume equivalent detection performance.

Tags: bot-and-agent-security, bot-mitigation, api-security, ddos, inventory, account-security, monitoring
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Security failures as retention and conversion risk
Use when: Making the business case for checkout security signals, privacy transparency, or remediating a security incident's customer-facing impact.
- Weigh the retention cost of incidents: the source cites a survey finding that 75% of consumers would stop using a site after an account takeover there and 87% would share the experience with others.
- Recognize the conversion cost of missing encryption: modern browsers flag any site without HTTPS with a 'Not secure' warning in the address bar, visible at the moment customers decide whether to enter card details.
- Use visible trust signals at the right point in the journey: the padlock icon and HTTPS prefix are the most widely recognized security signals for shoppers, Shop Pay stores returning users' shipping and payment details securely to reduce checkout friction, and third-party trust badges can supplement these on checkout pages — particularly for security-conscious categories like health products or high-value goods.
- Address privacy transparency as a conversion factor: the source cites a finding that 36% of consumers have stopped using a website due to privacy concerns, and GDPR requires clear information on what data is collected, why and how it is stored for EU/UK customers.
- Treat HTTPS and a padlock as baseline hygiene that removes a warning, not as proof of security — the source notes 98% of US web traffic on Google's platforms ran over HTTPS as of June 2026, making encryption an expectation, not a differentiator.
Caveat: Consumer survey percentages are third-party research snapshots; results in your store's audience may differ.
Caveat: Trust badges and privacy copy should not substitute for actual controls; false or outdated signals can worsen trust.

Tags: bot-and-agent-security, trust-signals, checkout, conversion-optimization, retention, privacy, https
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Privacy policy, GDPR exposure and third-party audit signals
Use when: Publishing or updating a privacy policy, supporting an EU/UK customer base, or evaluating what independent security assurance your platform provides.
- Confirm scope: if you sell to customers in the EU and UK, GDPR applies regardless of where your store is based.
- Publish clear information on what customer data is collected, why it is collected, and how it is stored; for Shopify-hosted stores, automated privacy policy templates cover core requirements and the Customer Privacy API supports cookie-consent banners that meet GDPR standards (verify current feature names and coverage).
- Understand the penalty scale: serious GDPR violations carry fines of up to 4% of a company's global annual revenue, with the source citing approximately €1.2 billion in EU supervisory authority fines in 2025 and average breach notifications around 443 per day (published figures, not predictions for your store).
- Use independent audits as diligence signals: the source states Shopify undergoes SOC 1 and SOC 2 audits every six months, verifying controls over customer data encryption, access management, incident response and physical infrastructure — check the current status and scope before citing it to customers or partners.
- Treat platform audit reports as covering the platform's environment only, not your store's apps, workflows or data handling.
Caveat: GDPR requirements and official templates change; verify current obligations with qualified counsel for your markets.
Caveat: SOC report scope and frequency can change — confirm the latest reports rather than relying on this description.

Tags: bot-and-agent-security, compliance, gdpr, privacy, soc-audit, data-handling, trust-signals
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Guaranteed chargeback coverage programs: eligibility and limits
Use when: Evaluating whether a guaranteed chargeback-coverage program applies to your store and how it changes your manual fraud-review workload.
- Check eligibility first: the source states Shopify Protect is available to eligible Shopify Payments users in the US — eligibility and geography matter, so verify current terms in the platform's help documentation.
- Understand what coverage does: orders are marked protected, payment is guaranteed, and if a dispute is filed on a protected order the platform covers the chargeback and the dispute fee.
- Use the covered-order marking to reduce manual review for orders that qualify, while keeping review in place for orders outside coverage.
- Reallocate the freed review time toward customer experience and high-value account management — the source quotes a merchant who said a staff member previously spent nearly her whole job on fraud and shifted to customer experience after switching to integrated fraud management.
- Do not assume all orders are covered; confirm which orders are marked protected in your admin before treating the program as your only fraud control.
Caveat: Program availability, eligibility and coverage terms are vendor-specific and subject to change — verify current terms.
Caveat: Coverage addresses chargeback liability on protected orders, not all fraud losses, false declines or operational costs.

Tags: bot-and-agent-security, fraud-prevention, chargebacks, shopify-protect, payment-security, operations
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Preventing card data from leaking outside checkout
Use when: Reviewing order-management, support and fulfillment workflows for card-data handling that could break compliance on an otherwise compliant platform.
- Instruct all staff never to ask customers for card details outside of checkout — any such request moves card handling into a non-compliant channel.
- Ban storing card numbers in order notes, emails, spreadsheets or shared documents used for fulfillment, support or record-keeping.
- When a customer sends card details by email or chat, treat the message as exposure: do not process it manually from that channel; direct the customer back to the compliant checkout flow.
- Apply the same rule to app and integration data flows: apps with order or customer permissions should not be used to store or relay raw card numbers.
- Recognize this is the merchant's practical PCI obligation on a hosted platform — the platform handles processing and storage in a compliant environment, and your role is not to introduce non-compliant handling.
Caveat: This guidance addresses card-data handling specifically; other customer data still carries privacy obligations under rules like GDPR.
Caveat: Individual staff workflows and third-party tools change — re-audit periodically.

Tags: bot-and-agent-security, pci-dss, compliance, data-handling, checkout, operations
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Prioritizing fraud controls when resources are limited
Use when: Building a fraud and security roadmap for a small store, deciding what to configure first, or allocating limited operational time to security work.
- Start with account protection since it gates everything else: enable 2FA on every admin account and add passkeys where supported — the platform can't protect an admin account with a weak or phishable credential.
- Then enable the platform's built-in fraud analysis and wire its risk ratings into automated order handling (auto-capture low risk, queue high risk for review) so fraud decisions do not depend on someone watching every order.
- Then reduce chargeback exposure financially: apply dynamic 3D Secure so higher-risk transactions carry step-up authentication and liability can shift to the issuer, and check eligibility for guaranteed chargeback-coverage programs.
- Then tighten verification settings like AVS and CVV carefully, watching for false declines on legitimate customers before changing defaults.
- Layer in organizational controls last but do not skip them: phishing training, app-permission audits, and prohibiting card data outside checkout — these address the human and integration paths that technical controls miss.
Caveat: No single control or sequence guarantees protection; each reduces specific risk and some increase false declines.
Caveat: Platform defaults, thresholds and feature availability change — verify current behavior before relying on any specific setting.

Tags: bot-and-agent-security, fraud-prevention, prioritization, account-security, 3d-secure, shopify, operations
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Assessing platform-level security defaults before you rely on them
Use when: Evaluating a hosting platform's security posture during store setup or migration, or documenting which security obligations remain with your team.
- Inventory the platform-provided defaults you can rely on: PCI DSS compliance by default, a free TLS certificate with HTTPS switched on by default, and card readers that are PCI and EMV compliant (per the source's Shopify description).
- Confirm fraud scoring exists and what signals it uses: one described implementation scores every order low/medium/high using AVS checks, CVV verification, IP address data, proxy detection and unusual purchase patterns.
- Check which optional programs and features you must explicitly enable or qualify for, such as guaranteed chargeback coverage, dynamic 3D Secure, and workflow automation apps.
- Document the residual merchant-side obligations — credentials, app permissions, staff access and customer-data handling — so platform defaults are not mistaken for complete coverage.
- Re-verify platform features and certifications periodically; vendor security offerings change and published descriptions may lag the interface.
Caveat: Platform feature descriptions here reflect a vendor blog source and may be outdated or specific to certain plans and regions.
Caveat: Default protections reduce risk but do not transfer all responsibility away from the merchant.

Tags: bot-and-agent-security, platform-security, due-diligence, pci-dss, tls, fraud-prevention, shopify
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Bot and fraud monitoring for inventory and high-demand drops
Use when: Planning a limited-release, high-demand drop, or investigating inventory that sells out unusually fast with suspicious buyer accounts.
- Treat inventory APIs as a defended surface: the source notes bots target API endpoints that handle checkout, inventory and customer account data, not only the storefront front end.
- Watch for the specific bot behaviors the source lists in ecommerce: card testing, pricing-data scraping, fake account creation, and stockpiling high-demand products before real shoppers can buy.
- Add friction proportional to risk on high-demand releases — for example, requiring authenticated accounts, limiting per-account quantities, and reviewing orders from newly created accounts.
- Monitor for early warning signs and act on them: the source describes a case where a platform's bot-detection tool flagged a major bot attack on Maggy London's storefront before any other monitoring system, illustrating the value of detection layered ahead of manual review (single case example).
- Keep account-creation defenses in place, since fake accounts are the base layer for hoarding and card testing.
Caveat: The Maggy London case is illustrative and does not guarantee similar detection performance.
Caveat: Inventory protection measures can create friction for legitimate customers; balance against conversion impact.

Tags: bot-and-agent-security, bot-mitigation, inventory, api-security, account-security, drop-management
Source: Ecommerce Security_ Threats and Best Practices.docx

---

## Four Pillars of Ecommerce Security: Privacy, Integrity, Authentication, Non-Repudiation
Use when: Auditing overall storefront security coverage, or deciding which control category a proposed security project belongs to.
- Assess coverage against four distinct pillars: Privacy (preventing unauthorized internal and external access to customer data — encryption, firewalls, antivirus), Integrity (accuracy of customer datasets — phone, address, purchase history), Authentication (proving the business is legitimate and customers are who they claim — 2FA or magic links), and Non-repudiation (neither company nor customer can deny a transaction, typically enforced via digital signatures).
- Map each existing control to a pillar; note gaps — for example, encryption addresses Privacy but does nothing for Authentication or Non-repudiation.
- For Authentication on the customer side, treat it as two-sided: credibility signals (customer quotes, case studies per the source) plus identity verification at transaction time.
- For Non-repudiation, plan how transactions are digitally signed so chargeback disputes and order denials have a verifiable record.
- Record which pillar each new security investment serves so overlapping projects are consolidated and uncovered pillars get funded.
Caveat: Non-repudiation is a concept the source explains generally; implementing digital signatures is a platform/payment-processor capability that should be verified for your stack.
Caveat: The source's suggestion to use customer quotes and case studies as 'authentication' evidence is a credibility measure, not a technical control — do not treat it as a substitute for account security.

Tags: bot-and-agent-security, platform-security, customer-accounts, checkout, compliance
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Multilayer Security: CDN Plus MFA as Defense in Depth
Use when: Designing or reviewing storefront defense architecture, especially before high-traffic launches or sales events.
- Adopt the source's multilayer principle: add secondary and tertiary controls so an attacker who defeats one layer must still penetrate at least one more before reaching data.
- Layer 1 recommended by the source: a Content Delivery Network; favor CDNs that use machine learning to block threats and infectious traffic.
- Layer 2: multifactor authentication for employees logging into company systems and for customers logging into loyalty accounts — requiring a second code sent via text, email, or authenticator app.
- Add firewalls as a further layer: firewall software and plugins allow trusted traffic while keeping untrusted connections off the site, which the source notes also makes anomaly detection easier and helps block XSS, spam, and SQL injection.
- Note that no single layer is sufficient; the value comes from combining controls so failures in one do not expose everything.
Caveat: The source does not claim any layer — CDN, firewall, or MFA — is individually sufficient; each can be bypassed.
Caveat: Verify current CDN threat-blocking capabilities and MFA mechanics against the vendor's current documentation, as these change over time.

Tags: bot-and-agent-security, platform-security, cdn, mfa, defense-in-depth
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Preventing E-Skimming at Checkout
Use when: Hardening the checkout page and payment flow against payment-data theft, or responding to a suspected checkout compromise.
- Understand the threat: e-skimming is stealing credit card and personal data from payment processors by gaining access to checkout pages and capturing payment information as customers type it in real time.
- Apply the source's three preventive measures: regularly push patches to your web server, vet your ad server code (injected ad scripts are a common skimming vector), and keep third-party APIs updated.
- Recognize that e-skimming can result from XSS, phishing, or brute force attacks, so closing those upstream vectors also reduces skimming exposure.
- If already impacted, the source advises checking whether cyber insurance covers losses and shutting down the shopping cart page while investigating and eliminating the source of the compromise.
- Treat checkout JavaScript and any third-party scripts loaded on the payment page as the highest-risk surface and inventory them regularly.
Caveat: The source's insurance and cart-shutdown guidance is a response outline, not an incident-response plan; consult qualified security and legal resources for a real breach.
Caveat: HTTPS/SSL alone does not stop e-skimming, since skimmers capture data before encryption in many cases — do not rely on SSL as the control.

Tags: bot-and-agent-security, checkout, payment-security, third-party-scripts, incident-response
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Reducing XSS and SQL Injection Risk Through Untrusted-Data Discipline
Use when: Reviewing custom storefront, theme, plugin, or API integration code for injection vulnerabilities.
- Train developers on the source's core rule: treat all edits to data tables as untrusted — SQL servers store data in tables retrieved by queries, and unprotected servers let attackers inject their own queries to view or change any data.
- Adopt modern web development technologies and frameworks that reduce raw query construction and unsafe output rendering.
- For XSS — where an attacker inserts malicious code into a page that exposes that page's visitors to phishing or malware — scan regularly for vulnerabilities in your website code and API integrations, and patch quickly.
- Vet every third-party API and theme/plugin integration as a potential injection path rather than trusting vendor code by default.
- Combine with firewalls, which the source notes help protect against XSS and malicious SQL injections by regulating traffic flow.
Caveat: Input validation and output encoding are the general defensive principle; the source only outlines this at a high level, so treat framework-specific implementation guidance as outside this note.
Caveat: No scanning tool guarantees complete coverage — regular scanning reduces, not eliminates, risk.

Tags: bot-and-agent-security, platform-security, xss, sql-injection, api-integrations
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Defending the Storefront Against Pricing and Inventory Scraping Bots
Use when: Protecting product pages, pricing data, and limited-inventory drops from scraping and cart-hoarding bots.
- Identify the business harm the source describes: bots scrape sites for pricing and inventory data, and attackers use that to hike prices or add the most popular inventory to their own carts, leaving customers unable to buy — leading to sales declines, negative reviews, and bad press.
- Deploy reCAPTCHA tools on the site, particularly on forms and entry points.
- Check and monitor your API connections, since bots often access inventory and pricing through APIs rather than rendered pages.
- Block older browser versions, which the source recommends as a bot countermeasure.
- Set up alerts for the three signals the source flags as bot indicators: unusually high web traffic, failed gift card validations, and repeated failed login attempts.
- Review whether your product feed or pricing API exposes full inventory levels to unauthenticated callers.
Caveat: CAPTCHA systems generate friction and change over time; verify current reCAPTCHA capabilities and consider accessibility impact before deploying broadly.
Caveat: The source's alert signals are indicators, not proof of bot activity — corroborate before taking blocking action that could affect real customers.

Tags: bot-and-agent-security, bot-mitigation, product-page, inventory, captcha
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Brute Force Protection for Admin Console and Customer Accounts
Use when: Securing the admin console, staff logins, or customer loyalty accounts against credential-guessing attacks.
- Understand the attack pattern: brute force attacks target an online store's administrator console, using automated scripts to guess every combination of letters, numbers, and characters that could form the password once a connection is established.
- Choose a complex, strong password for the admin panel and change it regularly.
- Ask customers to use complex, strong passwords for any loyalty accounts they create.
- Set up alerts for repeated failed login attempts, which the source lists as a sign of brute force attempts.
- Combine with multifactor authentication for employee system logins and customer loyalty logins so a guessed password alone is insufficient.
- Note the link the source draws: brute force is one of the upstream causes of e-skimming, so hardening login also reduces payment-data exposure.
Caveat: Password rotation intervals are a policy choice; verify current guidance, as forced frequent rotation can also encourage weaker passwords.
Caveat: Alerts only help if monitored and acted on — pair with lockout or rate-limiting controls.

Tags: bot-and-agent-security, authentication, admin-security, customer-accounts, brute-force
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Controlling Spam via Comment Cleanup, CAPTCHA, and Root-Cause Analysis
Use when: Cleaning up spam on storefront blogs, comment sections, contact forms, or review channels that could carry malicious links.
- Recognize spam's dual harm per the source: it prompts users to click malicious links and also slows browsing speeds on the site.
- Enable reCAPTCHA on forms — the source notes reCAPTCHAs require users to enter a slightly distorted series of characters that spambots cannot read.
- Delete spam comments that get through, keeping form response reports clean.
- Perform root cause analysis on spam that gets through to determine where it came from, which informs a durable fix rather than repeated cleanup.
- Note the source's observation that spam spreads via email as well as infected links left in blog comments, social media posts, and contact forms.
Caveat: CAPTCHA alone does not stop all spam, and the source treats deletion and root-cause analysis as complementary, not optional.
Caveat: Blog comment and review spam affects SEO and trust as well as security — evaluate both impacts.

Tags: bot-and-agent-security, spam, captcha, root-cause-analysis, forms
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## SSL Certificates: What They Do and Do Not Protect
Use when: Establishing or reviewing baseline transport security on a storefront, or explaining to stakeholders what SSL does and does not cover.
- Deploy an SSL (secure sockets layer) certificate, which per the source verifies a website's identity and serves as an encrypted connection.
- Rely on it to protect credit card details and other sensitive transaction data in transit, and to prevent attackers from using your site as part of a phishing attack.
- Treat SSL as one layer rather than the whole program — the source positions it alongside CDNs, firewalls, and antivirus/antimalware as separate best practices.
- Combine with checkout-page controls (patching, ad-code vetting, API updates) because SSL does not stop code injected into the checkout page from capturing data before transmission.
- On hosted platforms, confirm who provisions and renews the certificate under the platform's shared responsibility model.
Caveat: The source does not claim SSL alone secures a storefront; treating it as sufficient would leave skimming and account risks unaddressed.
Caveat: Certificate provisioning, renewal, and configuration specifics differ by host and change over time — verify against your platform's current documentation.

Tags: bot-and-agent-security, platform-security, ssl-tls, checkout, compliance
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Firewalls as Traffic Regulation for Anomaly Detection
Use when: Selecting or configuring perimeter controls for a self-hosted or platform storefront.
- Install firewall software or plugins that allow trusted traffic while keeping untrusted connections off the ecommerce site.
- Use the firewall to regulate traffic flow, which the source notes makes detecting anomalies easier and stops them before they enter the network.
- Rely on it particularly against the threats the source names: XSS, spam, and malicious SQL injections.
- Pair with a CDN layer and antivirus/antimalware scanning so the firewall is one layer in a multilayer approach rather than a standalone defense.
- On hosted platforms, check which firewall functions the platform provides versus what you must add — the source frames this under the shared responsibility model.
Caveat: Firewalls do not stop e-skimming injected via third-party scripts loaded in the browser, nor phishing aimed at customers.
Caveat: Misconfigured rules can block legitimate traffic and affect conversion — monitor for false positives after changes.

Tags: bot-and-agent-security, platform-security, firewall, traffic-analysis, defense-in-depth
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Inventory of Common Storefront Threat Types and Their Countermeasures
Use when: Building or reviewing a storefront security threat model and assigning owners to each countermeasure.
- Phishing — attacks that trick victims into providing confidential information via email, text, or phone, conveying urgency and mimicking trusted companies. Countermeasure the source highlights for merchants: inform customers you will never email or text to ask for personal information.
- Malware/ransomware — malicious software that disrupts or gains unauthorized access; ransomware encrypts files until payment. Counter with antivirus and antispyware, updated systems, and secure authentication.
- SQL injection and XSS — address through developer training, treating data-table edits as untrusted, vulnerability scanning, and quick patching.
- Brute force, e-skimming, and spam — apply strong admin passwords, checkout patching and ad-code vetting, and CAPTCHA plus comment cleanup respectively.
- Trojan horses — malware disguised as useful programs; counter with robust antivirus, firewalls, and reminding staff and customers to be wary of email attachments and unapproved third-party downloads.
- Ask staff and customers to avoid unapproved third-party downloads, since the source notes team members or customers may install Trojans themselves.
Caveat: The source explicitly relegates generic dictionary definitions of phishing, malware, ransomware, and Trojans to background rather than core material; the actionable part is the countermeasure mapping, not the definitions.
Caveat: Threat tactics evolve; treat this map as a starting inventory, not a current threat-intelligence feed.

Tags: bot-and-agent-security, threat-modeling, phishing, malware, training
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Separate malware detection from checkout fraud scoring
Use when: Reviewing order-review and fraud-screening controls for a storefront.
- Inventory storefront scripts, integrations and administrative devices exposed to malicious code.
- Use appropriate malware detection and patching on systems the merchant controls; a hosted storefront may restrict direct scanning or installation.
- Use payment-provider or fraud-platform risk signals to triage suspicious orders; antivirus software is not generally an order-fraud scoring system.
- Route uncertain high-risk orders for review and track false positives alongside fraud loss.
- Investigate both compromised checkout code and transaction abuse as distinct problems.
Caveat: Risk scores and malware scans have different scopes and neither proves an order is legitimate.

Tags: bot-and-agent-security, fraud-prevention, order-review, payment-security, risk-scoring
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Staff Security Training, Least Access, and Offboarding
Use when: Setting internal security policy for store staff, admin users, and departing employees.
- Ensure all employees are aware of the regulations that protect customer information.
- Enforce password updates and require employee cybersecurity and privacy training to decrease liability.
- Limit access to sensitive information so only staff who need customer data can reach it.
- Revoke access to all systems when employees leave — the source frames this as preventing ex-employees from selling data to attackers or committing cybercrimes themselves.
- Cover contractor and agency accounts that touch the admin panel, not just direct employees.
Caveat: The source does not set specific password-update intervals or training frequencies; treat these as policy decisions to verify against your compliance obligations.
Caveat: Offboarding is easy to overlook on hosted platforms where accounts proliferate — audit admin user lists periodically.

Tags: bot-and-agent-security, access-control, employee-offboarding, training, compliance
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Educating Customers on Password Hygiene and Phishing Risk
Use when: Setting customer account and loyalty login policy, or writing security-related customer communications.
- Acknowledge the source's premise: some security lapses come from customer behavior, particularly password reuse across many sites.
- Require long, complex passwords for customer accounts and loyalty programs.
- Remind customers about the risks of phishing attacks, and state plainly that you will never email or text to ask for personal information — the source's recommended countermeasure to phishing.
- Use multifactor authentication or magic links for customer logins so a reused password alone does not grant access.
- Set alerts for repeated failed login attempts against customer accounts as a detection backstop.
Caveat: Password-complexity requirements create checkout and account-creation friction; balance security against conversion impact for your store.
Caveat: Customer education reduces but does not eliminate phishing success — customers must still be protected by technical controls.

Tags: bot-and-agent-security, customer-accounts, authentication, phishing, retention
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Why Ecommerce Security Is a Business Priority, Not Just IT
Use when: Justifying security investment to store owners or stakeholders, or prioritizing security work against growth initiatives.
- Frame the stakes the source identifies: protecting customers' credit card and personal information is critical to building and maintaining your reputation as a trustworthy brand.
- Note the operational dimension: safeguarding your site ensures you have the financial and operational capabilities to deliver goods and services as promised.
- Make the customer-experience case: the source notes customers appreciate the extra steps taken to protect them, which can strengthen brand affinity.
- Acknowledge that baseline measures are common but insufficient, since attackers constantly change methods — merely hoping the right solutions are in place is not enough.
- Treat security as an ongoing program (patch cadence, scanning, training, monitoring) rather than a one-time implementation, and recognize that some ecommerce tools have built-in security features that adapt as practices emerge.
Caveat: Breach statistics cited in the source (such as hacker infiltration times and global breach volumes from Trustwave, DataProt, and Juniper Research) are illustrative context, not forecasts for any individual store.
Caveat: Building customer trust through security is a reasonable argument but the source provides no measured conversion or retention impact.

Tags: bot-and-agent-security, business-case, trust, platform-security, compliance
Source: Ecommerce security — what it means, common threats, and modern best practices.docx

---

## Least-privilege admin access for your store
Use when: You are adding a team member, agency, or contractor to your Shopify admin and deciding what access to grant.
- Map roles before granting anything: fulfillment staff, content editors, marketing, developer, finance. For each, list the specific admin areas they touch (orders, products, themes, apps, payouts).
- Assign only those permissions. Every additional admin account is a potential risk vector, so treat each grant as a security decision, not a convenience.
- Use time-limited access for temporary contractors — grant for the engagement window and revoke at the end.
- Audit access on a recurring basis (the source suggests regular audits) and immediately revoke permissions that are no longer needed.
- Where the platform supports custom roles, build role-based profiles rather than reusing a broad default.
- Pair with a real-time alert for suspicious admin activity so privilege misuse is visible.
Caveat: The source frames least privilege as baseline practice; the exact granularity of Shopify's role options changes over time, so verify the current interface in your admin settings.
Caveat: Least privilege is authorization (what a logged-in user can do) and does not replace authentication controls.

Tags: bot-and-agent-security, access-control, platform-security, shopify, admin-accounts
Source: How to Make Your Shopify Store More Secure.docx

---

## Two-factor authentication across every admin account
Use when: You are setting up admin security for staff, agencies, or yourself and deciding authentication requirements.
- Enable two-factor authentication for all store admin accounts without exception — the account owner included.
- Pick the method per the source's options: time-based one-time password, SMS code, or a hardware token. Where available, prefer stronger options like biometrics or hardware security keys over SMS, which the source lists alongside but is generally the weaker channel.
- Consider geolocation-based access restrictions as an additional layer where your platform allows it.
- Combine 2FA with an admin password policy and periodic compromise scans rather than treating it as the whole defensive stack.
- Review the list of admin accounts regularly so removed staff do not retain an authenticated path.
Caveat: 2FA is authentication, not authorization: it proves identity but does not decide what that identity may do.
Caveat: The source names these methods as available options; which methods your platform currently supports should be verified in current admin settings, not assumed fixed.

Tags: bot-and-agent-security, authentication, 2fa, admin-accounts, platform-security
Source: How to Make Your Shopify Store More Secure.docx

---

## Use unique admin credentials, MFA and compromise-driven password changes
Use when: You are writing the operating rules for who can log into your Shopify admin and how credentials are managed.
- Use long unique passwords managed in a password manager and enable strong MFA or passkeys where supported.
- Block known-compromised passwords where the identity system supports it.
- Change credentials when compromise is suspected or confirmed; do not adopt the source's arbitrary 60-90-day user-password rotation as a universal requirement.
- Revoke access, sessions and tokens during offboarding rather than waiting for a password change.
- Review login alerts and maintain a secure account-recovery process.
Caveat: This updates the source's rotation advice using current NIST guidance; service credentials may need a separate lifecycle policy.

Tags: bot-and-agent-security, authentication, password-policy, admin-accounts, credential-stuffing
Source: How to Make Your Shopify Store More Secure.docx

---

## Restrict and monitor admin panel login locations
Use when: You are hardening backend admin access against account takeover or rogue logins from unfamiliar locations.
- Implement IP whitelisting for admin panel access so only known networks can reach the backend.
- Set algorithms for geographic and time-based access restrictions where your platform or a supporting tool allows them.
- Limit or challenge login attempts originating from unfamiliar locations or devices.
- Build a real-time alert system that notifies you of suspicious administrative activity as it happens, rather than discovering it in a later audit.
- Keep and review activity logging so you can reconstruct what happened if an alert fires.
- This is defense-in-depth around the admin layer specifically — it sits on top of 2FA and least-privilege roles, not instead of them.
Caveat: IP whitelisting can lock out legitimate remote or traveling staff; plan exceptions deliberately.
Caveat: Exact IP/geolocation and alerting capabilities vary by platform and app, so verify what your current plan and tools actually support.

Tags: bot-and-agent-security, admin-accounts, account-takeover, monitoring, ip-whitelisting
Source: How to Make Your Shopify Store More Secure.docx

---

## Automate high-risk order handling with Shopify Flow
Use when: You are deciding how your store detects and acts on fraudulent or high-risk orders at scale.
- Rely on Shopify's built-in fraud analysis, which evaluates signals such as AVS/CVV matching and proxy IP detection to assign order risk levels.
- Layer 3D Secure checkout on payments where available: the source notes it authenticates the payment and can shift chargeback liability.
- Configure Shopify Flow to act on the risk indicators automatically — flag, hold, or cancel high-risk orders per your custom rules.
- Write rules that align with your specific business model rather than applying a single blanket threshold; high-value or high-shipping destinations may warrant different handling than routine orders.
- For stronger detection, consider additional ML-based fraud apps on top of the built-in system, reviewed for permissions before installing.
- Record what the automation did to each held/cancelled order so you can tune the rules and handle customer objections.
Caveat: Automated holds and cancellations can block legitimate orders; the source treats rules as business-model-specific, so test before scaling enforcement.
Caveat: Shopify Flow capabilities and available triggers/actions change; verify the current interface and available conditions.
Caveat: Fraud analysis is a risk signal, not proof of fraud.

Tags: bot-and-agent-security, fraud-prevention, shopify-flow, 3d-secure, payment-fraud, automation
Source: How to Make Your Shopify Store More Secure.docx

---

## Managing third-party app risk on a hosted platform
Use when: You are considering installing or pruning Shopify apps that touch your store's data, checkout, or admin.
- Maintain a detailed inventory of every installed app — what it does, who owns it, what data it reaches.
- Before installing anything, rigorously review the permissions the app requests and confirm each one is actually needed for the function you want. A poorly coded app can create a backdoor into the whole system.
- Review installed apps quarterly and remove unused or outdated plugins; each one is an entry point that does not earn its place.
- Prefer apps from trusted, well-reviewed developers and subscribe to security bulletins from Shopify and major app developers.
- When updating, read changelogs, check compatibility, and assess impact on store functionality rather than blindly updating.
- Treat third-party integrations as part of your attack surface when assessing API and data-breach exposure.
Caveat: The source's quarterly audit cadence is its recommendation, not a platform requirement; adjust to your app churn.
Caveat: Permission review reduces but does not eliminate third-party risk — a trusted app can still be compromised.

Tags: bot-and-agent-security, platform-security, third-party-apps, permissions, app-inventory
Source: How to Make Your Shopify Store More Secure.docx

---

## Shared responsibility: what you must secure on a hosted store
Use when: You are deciding where to focus your own security effort versus trusting the platform.
- Recognize the split: the platform handles underlying server infrastructure and default encryption; you own the administrative layer and configuration.
- Secure your side with HSTS, EV SSL certificates where relevant, access audits, 2FA, and least-privilege roles — the merchant-side controls the source lists.
- Do not assume that using a reputable platform means security is finished; the source states security is a collaborative effort between platform and merchant.
- Note that the source says default security mechanisms are the same across plans, including Plus — do not assume a higher plan alone buys you merchant-side protection.
- Assume default protections are continuously updated as threats evolve, but still layer your own controls on top.
- Review your store's URL shows https:// and a padlock, and that all resources load over HTTPS.
Caveat: This is the source's characterization of the shared responsibility model and Shopify's plans; plan features and compliance details should be verified against current Shopify documentation.
Caveat: HTTPS alone does not guarantee a secure store — it protects data in transit, not accounts, apps, or fraud.

Tags: bot-and-agent-security, platform-security, compliance, shared-responsibility, ssl
Source: How to Make Your Shopify Store More Secure.docx

---

## SSL, HSTS, and content encryption hygiene
Use when: You are auditing your storefront's transport security or debugging mixed-content warnings.
- Confirm your store URL begins with https:// and displays a padlock; HTTPS is enabled by default on the platform per the source.
- Implement HTTP Strict Transport Security (HSTS) so browsers cannot be downgraded to insecure connections.
- Check that all resources — images, scripts, stylesheets — also load via HTTPS; a single mixed-content asset undermines the padlock.
- For enhanced trust, the source mentions Extended Validation (EV) SSL certificates as an option.
- Treat SSL as requiring maintenance: continuous monitoring and periodic security assessments, not a one-time setup.
- SSL is transport-layer protection only — do not treat it as covering admin access or payment fraud.
Caveat: The source describes default SSL as enabled for all stores regardless of plan; current platform defaults should be confirmed rather than assumed.
Caveat: EV certificate availability and browser display behavior change over time; verify current browser and platform behavior before relying on it for trust signals.

Tags: bot-and-agent-security, ssl, https, hsts, platform-security
Source: How to Make Your Shopify Store More Secure.docx

---

## Backup strategy with versioning and geographic copies
Use when: You are designing business continuity so a breach, failure, or bad deploy doesn't lose store data.
- Set up automatic daily backups with versioning, using the platform's built-in features plus reliable third-party solutions where needed.
- The source recommends maintaining at least three copies of critical data on different resources, stored in geographically distributed cloud locations.
- Do not treat simple data duplication as a backup strategy — the goal is rapid recovery and business continuity, not just a copy.
- Regularly test backup restoration processes; an untested backup is an assumption, not insurance.
- Scope 'critical data' deliberately: product and order data, customer records, content, and configurations you cannot rebuild cheaply.
Caveat: The three-copies, geographically distributed rule is the source's recommendation (echoing common backup doctrine), not a platform-enforced setting.
Caveat: Hosted platforms may restrict what you can export or replicate; verify what your platform and chosen backup tools actually capture.

Tags: bot-and-agent-security, backups, business-continuity, platform-security, compliance
Source: How to Make Your Shopify Store More Secure.docx

---

## Code management standards for store developers
Use when: You have developers or agencies editing your theme, apps, or custom code and want review discipline.
- Treat code as a potential security risk: every change is an opportunity to introduce a vulnerability, so make review systematic.
- Use GitHub or a similar platform with security features for version control rather than editing directly on the live store.
- Establish a rigorous code review process, and per the source require at least two Shopify developers to approve significant changes to the codebase.
- Maintain strict development standards so reviews have criteria, not just a second pair of eyes.
- Keep an inventory of installed apps and themes so you know what code surface you are protecting.
- Pair with backup strategy so a bad deploy can be rolled back.
Caveat: The two-approver rule is the source's specific code deployment recommendation, not a platform requirement; it assumes you have at least two developers available.
Caveat: Version control protects against accidental or unreviewed changes, not against a malicious insider with merge rights.

Tags: bot-and-agent-security, code-security, version-control, platform-security, developer-process
Source: How to Make Your Shopify Store More Secure.docx

---

## Training staff to resist phishing and social engineering
Use when: You are setting up security training and reporting protocols for staff who access the store admin or handle customer data.
- Define clear protocols for every security-related work aspect — how to handle suspicious emails, unexpected payment or refund requests, and credential requests.
- Plan quarterly awareness training rather than a one-off onboarding session.
- Use real-world case studies and simulated phishing exercises to make the risk concrete.
- Create easily accessible reference materials so people can check protocol under pressure.
- Explain that phishing extends beyond email to domain spoofing and social media impersonation, and that credential theft often exploits reused passwords and missing multi-factor authentication.
- Make reporting suspicious activity easy and blame-free so incidents surface early.
Caveat: The quarterly cadence is the source's recommendation; frequency should reflect team size and turnover.
Caveat: Training reduces but cannot eliminate human error — keep technical controls (2FA, least privilege) in place regardless.

Tags: bot-and-agent-security, security-awareness, phishing, training, social-engineering
Source: How to Make Your Shopify Store More Secure.docx

---

## Mapping the fraud and abuse risks your store actually faces
Use when: You are deciding which security controls to invest in first for your store's specific model and exposure.
- Start by identifying which threats are relevant to your store rather than following a generic checklist; the source says define what's necessary for your store and prioritize accordingly.
- Consider the mechanisms behind each: credential theft is enabled by weak, reused passwords and absent MFA; account takeover then lets attackers change settings, run fraudulent transactions, and steal customer data.
- Treat unreliable integrations as a first-class risk: a single poorly coded app can open a backdoor, and API exposure grows with every integration.
- Recognize credential stuffing as automated reuse of breach databases — the defense is unique credentials plus 2FA plus login monitoring, not a single control.
- Malware can arrive via a poorly vetted app, a compromised theme, or an unsecured network connection, so vetting and network hygiene both matter.
- DDoS is operational: it can shut the store down entirely, causing revenue loss and reputational damage.
Caveat: This list is the source's enumeration of common ecommerce threats, not a quantified risk model for any particular store.
Caveat: Prioritization depends on your store's size, integrations, and payment model, which the source does not know.

Tags: bot-and-agent-security, threat-modeling, fraud-prevention, account-takeover, api-security, ddos
Source: How to Make Your Shopify Store More Secure.docx

---

## Evaluating payment gateways for fraud and encryption
Use when: You are selecting or reviewing a payment gateway for your store and weighing security alongside cost.
- Recognize that processors differ in encryption, fraud detection, and compliance standards, and that your choice affects your store's fraud and breach exposure.
- Conduct background checks on potential providers before integrating.
- Prefer Shopify-recommended providers; the source advises avoiding third-party gateways with negative feedback and limited security credentials.
- Confirm the provider offers solid encryption and fraud-detection mechanisms as part of the deal, not as an add-on.
- Layer 3D Secure where available to authenticate payments and reduce chargeback exposure.
- Separate this decision from the processing-fee comparison, which the source treats as a distinct concern.
Caveat: The source's recommendation to stick with platform-recommended gateways reflects its perspective; evaluate any specific vendor's current security claims directly rather than assuming.
Caveat: A gateway cannot compensate for weak admin security or a compromised app.

Tags: bot-and-agent-security, payment-fraud, checkout, gateways, compliance
Source: How to Make Your Shopify Store More Secure.docx

---

## Keep themes, apps and platform components updated
Use when: You are maintaining your store's software surface and deciding when to update or remove components.
- Maintain a detailed inventory of all installed apps so updates and removals are tracked, not ad hoc.
- Before updating, read technical documentation, changelog notes, check compatibility, and assess the potential impact on store functionality.
- Set up automatic updates where possible to avoid lag between patch and deployment.
- Review installed apps quarterly to remove unnecessary or outdated plugins — each retained plugin is a potential entry point.
- Subscribe to security bulletins from the platform and major app developers so you learn about vulnerabilities as they are announced.
- Treat this as covering themes as well as apps; an outdated theme is part of the same exposed surface.
Caveat: The quarterly review cadence is the source's recommendation; providers with active development or high sensitivity may warrant more frequent checks.
Caveat: Automatic updates can break customizations, so verify compatibility before enabling them broadly.

Tags: bot-and-agent-security, patching, third-party-apps, platform-security, maintenance
Source: How to Make Your Shopify Store More Secure.docx

---

## Using built-in fraud analysis and 3D Secure on the platform
Use when: You are assessing what protection your store already has by default before buying or configuring more.
- Know what you already get: default SSL encryption on all stores regardless of plan, 3D Secure checkout, built-in fraud analysis, Shopify Flow custom rules, and IP tracking that analyzes login attempts and flags high-risk buyers via proxy detection.
- Use 3D Secure checkout to authenticate payments and reduce fraudulent chargebacks.
- Use fraud analysis risk data to make per-order decisions; the source describes data-driven risk levels for each order.
- Extend with custom rules — for example, workflows that flag high-risk orders for review — aligned to your business model.
- Remember the source states default mechanisms apply across plans, including Plus, so plan upgrades don't change this baseline.
- Add third-party ML-based fraud apps only after reviewing their permissions, since these tools extend but also expand your attack surface.
Caveat: The source's claim that Plus security doesn't differ from regular accounts is its characterization at the time of writing; verify current plan features.
Caveat: Built-in fraud analysis is a signal layer, not a guarantee against chargebacks or all fraud types.

Tags: bot-and-agent-security, fraud-prevention, shopify, 3d-secure, platform-security, ip-tracking
Source: How to Make Your Shopify Store More Secure.docx

---

## Setting security priorities for a Shopify store
Use when: You are planning your store's security roadmap and deciding the first controls to implement.
- Begin with the source's framing that security is a comprehensive strategy, not a checklist — define what's necessary for your store first.
- Sequence the baseline controls the source presents: password policy, complex authentication, least-privilege access, admin access algorithms, gateway choice, SSL, updates, backups, code standards, fraud management, and awareness.
- Prioritize based on your store's risk profile — exposure depends on your integrations, team size, and payment model.
- Accept that the source's overall stance is that extra defensive layers are not excessive for an ecommerce store.
- Set a recurring review rhythm: access audits, app audits, awareness training, backup-restore tests.
- Revisit priorities as threats evolve, since both platform and attacker behavior change over time.
Caveat: The source's 'never overprotected' stance is an editorial opinion; over-layering controls can create operational friction and false positives, so weigh usability against risk.
Caveat: Specific cadences and rules in the source are recommendations, not platform requirements.

Tags: bot-and-agent-security, security-strategy, prioritization, platform-security, compliance
Source: How to Make Your Shopify Store More Secure.docx

---

## Distinguish agentic swarms from traditional bots to set detection scope
Use when: Deciding whether your storefront's current bot rules (rate limits, user-agent blocks, CAPTCHA) still fit actual traffic, or scoping a bot-management evaluation.
- Map your current bot defenses against the two categories: traditional bots are repetitive and predictable (price scraping, inventory hoarding, credential stuffing); agentic swarms interpret context and change behavior based on outcomes.
- Assume agentic traffic can pivot: when one approach is blocked, agents reportedly shift user agents, proxies, and tactics mid-run rather than repeating a failing pattern.
- Do not treat 'bot' as a single threat class — separate legitimate shopping assistants (research, catalog browsing) from malicious automation in your policy design, since they can look similar.
- Re-baseline detection rules to flag behavior changes over a session (new user agent, sudden scope change) rather than relying on static identifiers alone.
- Prioritize protection of high-value actions — checkout, account changes, loyalty balances — rather than uniform blocking across all traffic.
Caveat: The autonomy distinction is a conceptual framing; no rule set cleanly separates the two categories in production, and both can share the same infrastructure.
Caveat: Mid-attack self-rewriting capability is described in the source as a threat characteristic; verify against your own observed traffic before assuming your adversaries operate this way.

Tags: bot-and-agent-security, bot-management, detection, traffic-analysis, fraud-prevention
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Signal masking: don't misread legitimate headless agents as fraud
Use when: Investigating high false-decline rates on API or headless traffic, or tuning WAF/CAPTCHA rules that block legitimate AI shopping assistants.
- Audit which current defenses depend on client-side signals — invisible CAPTCHAs, honeypot form fields, device fingerprinting, UI interaction cues — since headless API agents never render those elements and fail them by default.
- Trace decline reasons on blocked traffic to separate 'no client-side telemetry' (a signal about the channel, not intent) from actual malicious patterns.
- Add intent and behavior signals that work for API traffic — declared purpose, endpoint sequence, account recognition, session consistency — instead of relying on human-interaction cues.
- Be aware the same masking cuts both ways: malicious swarms reportedly mimic human micro-behaviors to evade behavioral biometrics, so no single signal should be the sole basis for blocking or permitting.
- Move stringent verification to transactional points (checkout, account modification) and let research-stage browsing pass more freely.
Caveat: The source reports that a majority of monitored AI bot activity is allowed to pass unrestricted for lack of granular differentiation — a claim from the report's cited sources, not a universal benchmark.
Caveat: Reducing client-side checks to avoid false declines also removes signals used against human-impersonating automation; compensate with other layers.

Tags: bot-and-agent-security, false-declines, bot-management, waf, conversion-optimization, headless-agents
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Passport/immigration model: layer cryptographic identity with behavioral checks
Use when: Designing how verified shopping agents get access to your storefront, or evaluating vendor agent-authentication offerings.
- Adopt the two-role framing: the identity protocol (e.g., Visa TAP, Skyfire KYA, WBA) acts as the passport; edge behavioral intelligence acts as the immigration officer.
- Never rely on the credential alone — a verified agent from a compromised server, or one that enters declaring browsing intent then starts scraping or testing cards, should still be stopped by behavior analysis.
- Capture the agent's stated intent at entry (browsing vs. paying, consumer recognition, payment information where applicable) and compare it against observed actions for the rest of the session.
- Continuously re-evaluate in-session: if behavior changes after entry, re-challenge or remove the visitor rather than trusting the initial verification.
- Assign differentiated permissions by trust tier instead of a single verified/unverified binary.
Caveat: Cryptographic identity does not guarantee benign behavior — the source explicitly pairs it with behavioral monitoring for this reason.
Caveat: Protocol names, supporting vendors, and integration details change; confirm current capabilities and supported standards with the vendor before committing architecture.

Tags: bot-and-agent-security, agent-authentication, intent-detection, edge-security, visa-tap, trust-tiers
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Adaptive response: permit, verify, challenge, prevent by risk tier
Use when: Defining checkout, account, and browsing traffic policies, or configuring a bot-management platform's response actions.
- Permit low-risk agent interactions such as browsing and product discovery — legitimate agents need broad research access before transacting.
- Verify sessions when behavioral signals shift (e.g., declared browsing but scanning many accounts or endpoints).
- Challenge with step-up authentication when financial or account risk emerges — loyalty point changes, shipping address changes, high-risk transactions.
- Prevent malicious automation executing high-risk actions outright.
- Enforce these decisions at the CDN/edge before traffic reaches downstream systems, so controls apply before fraud propagates and without adding latency.
- Reassess continuously within a session rather than deciding once at entry.
Caveat: The four-action permit/verify/challenge/prevent model is attributed to Darwinium in the source; treat it as one vendor framework among several, not a standard.
Caveat: Thresholds for 'low risk' vs. 'financial risk' are not specified and must be set from your own baseline data.

Tags: bot-and-agent-security, adaptive-response, edge-security, checkout, step-up-authentication, policy-enforcement
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Prevent agent hijacking and account takeover of stored credentials
Use when: Hardening customer accounts, saved payment methods, and third-party agent access, or investigating suspicious account modifications.
- Treat any agent acting on behalf of a customer account as a potential hijack vector — compromise of a legitimate agent's credentials lets attackers act as the agent.
- Require risk-based step-up authentication (MFA) specifically for sensitive actions: changing delivery address, extracting payment data, draining loyalty points or gift-card balances.
- Apply micro-authorization: grant each agent action only the minimal permission it needs, so a hijacked agent has a small blast radius.
- Microsegment back-end systems so a compromised agent cannot move laterally across the platform.
- Monitor for rapid gift-card balance brute-forcing and credential-stuffing against loyalty accounts, which the source says swarms can drain quickly.
Caveat: Risk-based MFA thresholds are not specified; set them from your own risk model.
Caveat: If legitimate agents are used by real customers, blocking all credential use harms conversion; the control should be scoped to high-risk actions.

Tags: bot-and-agent-security, account-takeover, agent-hijacking, risk-based-mfa, loyalty-fraud, gift-cards, micro-authorization
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Multi-agent attack patterns: trust asymmetry, context loss, delegation loops
Use when: Threat-modeling an agent-integrated storefront or evaluating what an automated shopping/assistant integration is permitted to do.
- Do not let downstream systems act on instructions relayed by another agent without verifying the original source — a specialist agent performing an action 'because a teammate relayed it' is the trust-asymmetry failure to avoid.
- Preserve context through delegated steps: the agent executing the final action must know it involves sensitive data, or it will authorize something it shouldn't.
- Watch for delegation loops — circular task delegation that exhausts resources and never completes, which attackers can induce through planted links or forms that require another agent's involvement.
- Split-anomaly awareness: malicious behavior distributed across multiple sites/agents may leave no single step looking anomalous, so judge the end-to-end session, not just individual requests.
- For ecommerce automation: require each agent action to be independently authorized against the merchant's policy rather than inherited from a peer's approval.
Caveat: These named attack patterns come from academic research (arXiv/Princeton) as reported in the source; treat them as illustrative threat models to test against, not confirmed incidents at any specific retailer.
Caveat: The source's examples are agent-framework scenarios; mapping to a live storefront requires your own validation.

Tags: bot-and-agent-security, multi-agent-attacks, threat-modeling, prompt-injection, agent-delegation, authorization
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Treat prompt injection and untrusted content as an authorization problem for storefront agents
Use when: Anyone deploying a customer-facing chatbot or AI agent that reads external content (reviews, forums, supplier data) or holds operational authority.
- Assume any content an agent reads — product descriptions, reviews, third-party feeds, support messages — is untrusted data, not instructions the agent may act on.
- Treat input filtering as one signal; enforce action permissions and business rules outside the model even when the prompt or retrieved content is malicious.
- Limit the operational authority of any back-end conversational agent so a successful injection cannot reach sensitive actions or data.
- Guard against data poisoning: validate and monitor the data sources agents use for decisions, since corrupted sources cause cascading failures across connected agents.
- Block AI token freeloading: detect and reject traffic routing unrelated model queries or training workloads through your public AI endpoints, which degrades performance and raises your infrastructure costs.
- Grant tools and API access by scope — an agent reading catalog data should not also hold payment or admin credentials.
Caveat: No prompt filtering alone guarantees safety; pair input sanitization with scoped permissions and monitoring.
Caveat: The source describes these as documented threat vectors and OWASP-category risks; exact exploit mechanics and current OWASP numbering should be verified against the latest OWASP Agentic AI guidance.

Tags: bot-and-agent-security, prompt-injection, chatbot-security, data-poisoning, input-sanitization, least-privilege, api-hardening
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Defend storefront APIs: continuous endpoint discovery and Layer 7 DDoS awareness
Use when: Auditing API exposure, preparing for card-testing or scraping attacks, or planning edge capacity ahead of a product drop.
- Continuously discover and map APIs — including undocumented and internal endpoints — because swarms reportedly target unprotected endpoints for scraping and token freeloading.
- Identify which APIs expose sensitive data; the source reports most commerce respondents could not say which of theirs did, so this gap is a common starting point.
- Apply intent-based detection at the edge on API traffic, not just on browser traffic, since headless agents bypass client-side controls.
- Prepare for Layer 7 volumetric floods at the CDN/edge so downstream systems are not impacted before controls apply.
- Detect automated card-testing patterns (high volumes of small authorization attempts, distributed across identities) and respond with adaptive actions rather than blanket blocks.
- Micosegment API back ends so an exploited endpoint has a contained blast radius.
Caveat: The incident and DDoS statistics in the source are organization-specific findings from its cited reports; use them to justify diligence, not as your expected baseline.
Caveat: Attribution of a traffic spike to malicious bots requires validation — legitimate agents and promotions can produce similar patterns.

Tags: bot-and-agent-security, api-hardening, api-discovery, ddos, card-testing, edge-security, microsegmentation
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Counter inventory hoarding and price scraping without blocking legitimate agents
Use when: Protecting high-demand product drops, protecting price data, or tuning policies for scraping traffic on catalog and PDP endpoints.
- Segment traffic by action: allow broad catalog research but apply stricter verification at add-to-cart and checkout, where hoarding actually occurs.
- Watch cart-abandonment patterns at scale — inventory claimed by bots that never converts creates artificial scarcity; track conversion of cart-reservations against account authenticity.
- For price scraping, verify intent against declared purpose: an agent that declared browsing but systematically extracts catalog and pricing data at volume is showing intent drift.
- Use AI-resistant challenge mechanisms (e.g., dynamic QR-code flows) for high-risk actions on drop pages, which the source frames as making automated fraud economically unviable.
- Consider a virtual waiting room or priority lanes for drops to give trusted agents and humans differentiated access instead of a single queue or hard block.
- Dynamically modify page elements that automated agents read or click, and add verification steps for higher-risk actions.
Caveat: Blanket-scraping defenses can block legitimate comparison-shopping agents and cost you sales; the source's own posture is to welcome legitimate agents while stopping malicious automation.
Caveat: AI-resistant challenge efficacy is presented as an emerging vendor approach; validate against your own attacker patterns and accessibility requirements.

Tags: bot-and-agent-security, inventory-hoarding, price-scraping, product-drops, scarcity, challenge-design, merchandising
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Build dedicated agent rails and micro-authorization for verified agents
Use when: Architecting how third-party shopping agents and assistant integrations access your catalog and checkout.
- Establish dedicated 'agent rails' — isolated, purpose-built pathways for verified agents — instead of opening the same interface to everything or blocking all automation.
- Grant minimal necessary permissions per agent action (micro-authorization), so a hijacked or poisoned agent cannot reach beyond its task.
- Enforce policy-based access controls that distinguish verified agents, humans, and unverified automation, with different rights per class.
- Ensure agent access to user-specific flows is reviewed for data protection implications before enabling it.
- Keep decisions at the edge in real time so policy is applied before traffic touches downstream systems.
- Define and document what each trust tier may do: allow, monitor, rate-limit, authenticate, or block.
Caveat: Dedicated rails require knowledge of which agents are legitimate; without cryptographic verification or a directory, 'rail' access becomes an open door.
Caveat: The source acknowledges retailers risk disintermediation and reduced customer insight as agents become intermediaries — an architectural trade-off, not only a security one.

Tags: bot-and-agent-security, agent-rails, least-privilege, access-control, api-hardening, trust-tiers, checkout
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Run a visibility-and-baseline phase before changing bot policy
Use when: Kicking off a bot-management program or being asked to block 'all bots' on a storefront.
- Audit current bot detection and WAF configurations to document what is actually being blocked, challenged, and allowed today.
- Identify all APIs and endpoints exposed to agent traffic, including undocumented ones.
- Baseline current AI agent activity: which agents, which pages/endpoints, and what stated or inferred intent (indexing, comparing, extracting).
- Document existing policies around automated access — many organizations have informal rules never written down.
- Only after baselining, move to defining allow/monitor/rate-limit/authenticate/block policies and trust tiers.
- Pair this with the readiness questions: can you identify which agents access the site, where they go, and why.
Caveat: The source's suggested timeline (Weeks 1–4 visibility, 3–6 policy, 5–12 implementation) is a planning heuristic, not a validated schedule; adjust to your scale and risk.
Caveat: Baselines go stale as agent traffic grows; re-run the baselining periodically.

Tags: bot-and-agent-security, assessment, baseline-mapping, api-discovery, policy-design, implementation-roadmap
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Define a documented AI agent access policy with trust tiers
Use when: Writing or revising an acceptable-use/automated-access policy, or aligning privacy policy and terms of service with agent traffic.
- Classify agent interactions by category (indexing, price comparison, shopping assistance, payment) and assign each a trust tier with permitted actions.
- Decide per tier whether to allow, monitor, rate-limit, authenticate, or block — and record the decision so enforcement is consistent.
- Define escalation and human-in-the-loop thresholds for ambiguous or high-risk sessions.
- Align privacy policy and terms of service with agent interactions, and assess data-protection implications of agent access to user-specific flows.
- Make sure each policy can be technically enforced (block, rate-limit, authenticate) — a policy you cannot enforce is documentation, not control.
- Review whether your privacy policy addresses AI agent interactions at all, which the readiness checklist calls out as a common gap.
Caveat: Trust-tier boundaries are business decisions, not standard values; the source provides the categories and checklist, not thresholds.
Caveat: Regulatory expectations (NIST AI RMF, OWASP Agentic AI Top 10) emphasize documentation, monitoring, human oversight, and context-sensitive controls — treat these as direction, and verify current versions.

Tags: bot-and-agent-security, policy-design, governance, trust-tiers, compliance, privacy, terms-of-service
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Reconcile 'block the bots' thinking with agentic commerce reality
Use when: When leadership or an agency pushes a blanket bot-blocking rule, or when false declines or lost agent-driven sales surface.
- Reframe the objective from 'human vs. bot' to managing traffic by intent and trust level — the source calls this 'agentic readiness'.
- Measure both failure directions: revenue lost from false declines of legitimate agents, and losses from malicious automation that passes.
- Assign different access levels based on agent identity, behavior, and business relationship rather than a single allow/block decision.
- Set policy per endpoint and action (browsing vs. checkout vs. account modification) because the right friction differs by stage.
- Plan for the customer-relationship trade-off: as agents intermediate, retailers risk reduced customer insight, loyalty, and cross-selling, so decide which flows you keep on-site and instrumented.
Caveat: The 'split-brain' framing and the trust-based posture are attributed to Akamai's Reuben Koh and the report; competing vendors may argue for stricter blocking.
Caveat: The source notes consumers currently trust retailers' on-site agents more than off-site third-party agents — a reported finding that can change; verify current sentiment before betting architecture on it.

Tags: bot-and-agent-security, agentic-commerce, strategy, intent-detection, false-declines, customer-data
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Map identity and authentication protocols before committing to vendors
Use when: Choosing or evaluating agent-authentication or bot-management vendors for an ecommerce stack.
- Separate agent identity, represented user or merchant, and permission to perform the requested action.
- Ask vendors to demonstrate current supported issuers, validation, revocation, audience binding and replay protection.
- Test whether a valid identity can be denied an out-of-scope action, including an action against another store's data.
- Confirm interoperability using the actual implementation rather than announcement-level support lists.
- Document fallback and credential-expiry behavior before enabling payment or account-changing operations.
Caveat: Protocol names and partnerships in the source are unverified snapshots; no vendor support or universal interoperability is assumed.

Tags: bot-and-agent-security, agent-authentication, vendor-evaluation, visa-tap, kya, web-bot-auth, standards
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Use a readiness checklist to expose gaps in agent-visibility and enforcement
Use when: Running a periodic security review or preparing for an agent-traffic surge such as a product launch.
- Visibility: confirm you can identify which AI agents access the site, which pages/endpoints they visit, and why they visit (indexing, comparing, extracting).
- Governance: confirm you have a documented AI agent access policy, know which actions to allow vs. block, and can technically enforce the policy (block, rate-limit, authenticate).
- Privacy/compliance: confirm the privacy policy addresses agent interactions and that data-protection implications of agent access to user-specific flows are understood.
- Security/fraud: confirm you can detect malicious agent behavior, protect against agent takeover, impersonation, and abuse, and automatically block unwanted or untrusted agents.
- For each unchecked item, assign an owner and a concrete control (endpoint instrumentation, rate-limit rule, authentication requirement).
- Re-run the checklist after any major change in agent traffic or integration.
Caveat: The checklist is DataDome's readiness framing as reported in the source; treat unchecked items as prompts to investigate, not as a certified standard.
Caveat: Passing every item does not guarantee protection — the checklist covers visibility and policy, not attack efficacy.

Tags: bot-and-agent-security, readiness-assessment, audit, policy-design, monitoring, fraud-prevention
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Stand up continuous monitoring and red-teaming after deployment
Use when: Operating a live bot-management program after initial deployment, or setting a review cadence for agent traffic policy.
- Monitor agent activity dashboards and verification results regularly, watching for new agent categories and shifts in verification pass/fail rates.
- Tune policies against observed behavior and emerging threats rather than set-and-forget configurations.
- Conduct regular red-team exercises simulating agentic swarm attacks — multi-agent delegation, prompt injection through processed content, scraping and card-testing patterns — on systems you own and are authorized to test.
- Update defenses as new protocols and standards emerge, since the identity and authentication landscape is still forming.
- Validate that edge enforcement applies before downstream impact and does not add latency to legitimate traffic.
- Keep the visibility baseline from Phase 1 fresh so deviations remain detectable.
Caveat: Red-teaming must be authorized and scoped to owned systems; do not test attack patterns against third parties.
Caveat: The source gives no benchmark for how often to red-team or tune; choose a cadence based on traffic volume and change rate.

Tags: bot-and-agent-security, monitoring, red-teaming, continuous-improvement, policy-tuning, edge-security
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Model the fraud cost multiplier when justifying bot-defense spend
Use when: Building a budget justification for bot management, or estimating exposure from card-testing and hoarding.
- Use the total-cost framing rather than direct-loss framing: chargebacks, operational handling, and lost product all attach to a single fraudulent transaction.
- Estimate your own multiplier from internal data where possible — chargeback fees, support handling time, replacement/restocking costs — instead of assuming the source's figure.
- Add indirect losses that multipliers often miss: inventory hoarded but never converted, price data scraped and undercut, loyalty/gift-card balances drained.
- Present both directions of loss: fraud losses and false-decline revenue loss from blocking legitimate agents, since the second is easy to overlook.
- Pair the cost case with the readiness gaps (unknown sensitive APIs, no documented policy) to prioritize the highest-exposure work first.
Caveat: The $5.13 multiplier and the cited traffic/fraud statistics come from the source's cited reports and reflect specific measurement periods; treat them as directional, not as your store's actual economics.
Caveat: Attributing revenue loss to false declines requires instrumentation most stores lack; estimate conservatively or label it an assumption.

Tags: bot-and-agent-security, fraud-prevention, cost-analysis, business-case, chargebacks, measurement
Source: Protecting E-Commerce from Agentic Swarms and AI Bot Attacks_ A Comprehensive Security Report.docx

---

## Map your ecommerce attack surface by target: browser, server, client app, user
Use when: Planning a security review or threat model for an online store, deciding which defenses to prioritize across storefront, checkout, and admin surfaces.
- Enumerate what runs where on your store: the browser sandbox (how your site is isolated from other tabs the shopper has open), the server (your web app and APIs), the client app (the JavaScript, including anything embedded such as third-party ad or widget code), and the shopper themselves (accounts, credentials, tracking exposure).
- For the server angle, assume the client is not yours to control: a shopper or attacker can send any HTTP request a normal browser would never send (the source demonstrates this with a raw curl request), so enforce every rule server-side rather than relying on hiding UI buttons.
- For the client-app angle, look for any way a crafted URL or embedded third-party script can make your pages run code they weren't meant to run — the source cites McDonald's-style cross-site scripting where merely visiting a link could leak a password.
- Treat third-party ad/embed code as running in a neighboring context that must not be able to touch the rest of the page.
- Document, per surface, which money- or data-bearing actions (checkout, admin edits, refunds, address changes) require elevated checks.
Caveat: The source's four-way framing is a teaching model, not a certification standard; the specific attacks shown (localStorage exhaustion, clickjacking) were fixed in major browsers at the time and may or may not apply now — verify current browser behavior.
Caveat: A secure-looking UI is not a server control; the source explicitly warns the client can be modified.

Tags: bot-and-agent-security, threat-modeling, checkout, storefront-security, third-party-scripts, xss
Source: Site Security (1).docx

---

## Make endpoints safe even when the client lies (tampering with prices, quantities, roles)
Use when: Building or auditing cart, checkout, discount, order, or admin endpoints where a shopper could bypass the UI's intended path.
- Assume any request your front end can generate can also be generated by hand with modified parameters — the source's core server-side lesson is that you don't control the client because it runs on the user's machine and can be rewritten.
- For each state-changing endpoint (add-to-cart, apply-discount, change-quantity, submit-order, edit-account, admin actions), define explicitly what inputs are allowed and reject everything else.
- Never trust client-supplied values that should be authoritative server-side (item prices, totals, discount eligibility, user role, free-shipping thresholds); recompute them server-side from trusted data.
- Re-authorize on every request: confirm the acting user is permitted to perform that action on that specific resource, not just that they are logged in.
- Add server-side rate limits and anomaly logging on sensitive endpoints so automated abuse is visible even if individual requests look valid.
Caveat: The source frames this as a mindset, not a checklist; specific validation libraries and framework behaviors change — verify your framework's current guidance.
Caveat: This mitigates request tampering, not account takeover or credential theft, which need separate controls (see authentication cards).

Tags: bot-and-agent-security, checkout, pricing, authorization, input-validation, api-security
Source: Site Security (1).docx

---

## Distinguish a vulnerability from an exploit when triaging storefront findings
Use when: Prioritizing a pentest or bug-bounty report on your store, or deciding how urgently to patch a reported issue.
- Classify each finding: is it a bug/weakness that could be abused (vulnerability), or a working, deployable attack (exploit)? The source defines vulnerability as the bug itself and exploit as the code that takes advantage of it.
- Treat a confirmed exploit against a live customer-facing surface (checkout, payment, account) as urgent; treat a latent vulnerability as something to schedule and remediate with defense-in-depth.
- For a vulnerability you cannot immediately fix, add compensating controls (server-side checks, logging, rate limiting, WAF rules) rather than waiting for a perfect patch.
- Follow responsible disclosure: the source points to the Stanford bug-bounty process as a model — don't attack in ways that destroy or delete data, and ask before acting if unsure.
- When paying for external testing or bug bounties, scope strictly to systems you own so you are not authorizing attacks on third parties.
Caveat: This card adapts a security-course distinction to store operations; the source gives no ecommerce remediation timelines or SLAs — set those from your own risk tolerance and any regulatory requirements.
Caveat: Bug-bounty process details referenced (e.g., university program rules) are institution-specific and may not transfer to your business.

Tags: bot-and-agent-security, vulnerability-management, bug-bounty, incident-response, risk-prioritization
Source: Site Security (1).docx

---

## Prevent storefront XSS with context-aware rendering
Use when: Handling any shopper- or admin-supplied content that gets displayed on your storefront — reviews, product Q&A, profile names, search terms, order notes, support messages, or header values.
- Trace untrusted product reviews, profile fields, search parameters and imported content to their rendering locations.
- Use framework auto-escaping and safe text APIs for plain text; encode at output for the actual context.
- Do not apply HTML entity encoding as a universal solution for JavaScript, CSS or URL contexts; avoid inserting untrusted data in executable contexts.
- Where rich HTML is required, use a maintained sanitizer with a restricted policy.
- Add a tested CSP as defense in depth and validate harmless stored/reflected cases on an owned test environment.
Caveat: CSP and escaping are complementary; neither replaces authorization or secures every injection context alone.

Tags: bot-and-agent-security, xss, output-encoding, input-validation, product-reviews, third-party-scripts
Source: Site Security (1).docx

---

## Use stored-injection defenses against self-propagating content worms in user-generated store content
Use when: Designing or reviewing user-generated content surfaces on a store — reviews, Q&A, wishlist sharing, profile pages, social/community features, seller or marketplace listings.
- Recognize the worm pattern: the source's MySpace/Samy case shows injected code in a profile executing automatically for visitors and spreading without further attacker action — the storefront equivalent is content that runs for every shopper who views a page.
- For any surface where one shopper's input is rendered to other shoppers, escape control characters at output so the input is text, not code.
- Contain blast radius: limit the privileges of the context in which rendered content runs, and don't let UGC-bearing pages hold more session authority than needed.
- Add moderation, allow-listed markup for rich content, and monitoring for sudden spikes in a page's outbound requests or injected patterns.
- Test with a known-safe, owned staging environment rather than live customer data — the source's classroom demos are illustrative, not instructions to attack production.
Caveat: Historical examples (MySpace worm) describe a platform and era whose mitigations differ from today's browsers and frameworks; treat the pattern as the lesson, not the exact mechanism.
Caveat: Encoding prevents script execution but does not by itself stop spam, scams, or abusive content — those need separate moderation controls.

Tags: bot-and-agent-security, xss, user-generated-content, product-reviews, moderation, defense-in-depth
Source: Site Security (1).docx

---

## Guard admin accounts against privilege-escalation chains in your CMS or store platform
Use when: Reviewing admin access, CMS/content tooling, plugin ecosystems, or any surface where store staff with elevated privileges view attacker-influenced content.
- Study the source's WordPress case: code was posted into the database, rendered on a page, and — because the viewing user was an admin — used that admin's authority to create a new admin user with attacker-chosen credentials, which the attacker then tried across many WordPress installs.
- Ensure no stored content rendered to an admin can trigger privileged actions; separate 'view content' from 'perform admin mutations' with explicit re-authorization.
- Apply least privilege: only the accounts genuinely needing admin rights should have them, and admin session actions should require fresh confirmation.
- Require strong, unique admin credentials and enable multi-factor authentication so a harvested credential set can't be replayed across installs.
- Inventory third-party plugins/themes and content sources that can write into pages your staff view, and log admin-account creation as a monitored event.
Caveat: The WordPress incident is a historical case study, not a current guarantee about any platform; verify your CMS's current patching and plugin-review posture.
Caveat: The source does not quantify how many installs were affected beyond describing a broad campaign; treat it as an illustration of the escalation pattern.

Tags: bot-and-agent-security, authentication, authorization, admin-security, privilege-escalation, cms-security, stored-xss
Source: Site Security (1).docx

---

## Audit your dependency supply chain for typosquatting and unreviewed packages
Use when: Selecting and maintaining storefront frameworks, cart plugins, payment SDKs, or any npm/composer/PyPI dependency that ships to your site or servers.
- Treat every dependency as code you are shipping: the source notes npm install React pulls in code from many contributors, so full manual audit isn't realistic — accept that and manage the risk instead.
- Watch for typosquatting: attackers register names similar to popular packages, and enough people typo the install to generate real adoption. The source's example code simply pinged a server but otherwise worked like the real package, so users didn't notice, and it reportedly ran ~45,000 times across 17,000 domains including .mil systems.
- Mitigate by locking dependency versions, reviewing new direct dependencies before adding them, preferring well-maintained packages, and monitoring lockfiles for unexpected changes.
- Note that registries have added defenses (the source says npm began rejecting names too similar to popular packages), but these are not complete — verify current registry protections rather than assuming safety.
- Keep an inventory of which third-party code runs on customer-facing pages versus server-side, so a compromised package's blast radius is known.
Caveat: The typosquatting example is an anecdotal demonstration; the 45,000-run/17,000-domain figures are the source's report of one incident, not a benchmark for your risk.
Caveat: Registry defense mechanisms change over time — verify what your registry currently enforces.

Tags: bot-and-agent-security, supply-chain, dependencies, npm, third-party-scripts, software-composition
Source: Site Security (1).docx

---

## Deploy multiple independent defenses so one unknown bug doesn't expose the store
Use when: Architecting a new storefront feature or reviewing an existing checkout/account flow where a single control currently stands between attacker and customer data.
- Accept the source's premise: you cannot fully audit or prove your code (or your dependencies) secure — defenders face bias and hidden bugs that an attacker just has to find once.
- For each high-value asset (payment data, customer PII, admin control), identify the single point of failure and add a second, independent control — e.g., server-side validation in addition to input encoding, or re-authentication in addition to a session check.
- Assume a control will fail: design the system so that if escaping, validation, or a WAF misses something, the impact is contained rather than total.
- Layer defenses across layers — browser-side, server-side, and process controls — rather than concentrating effort in one place.
- Re-examine assumptions after any incident or near-miss, since a hidden bug in a dependency can persist unnoticed.
Caveat: Defense-in-depth reduces but does not eliminate risk; the source is explicit that no system can be known to be fully secure.
Caveat: Never present layered controls as a guarantee — each layer has its own failure modes.

Tags: bot-and-agent-security, defense-in-depth, architecture, checkout, risk-management, threat-modeling
Source: Site Security (1).docx

---

## Distinguish user consent / permissions from actual security when adding storefront permissions
Use when: Deciding whether to adopt a browser feature or third-party script on your store — live chat with camera, AR try-on, GPU-heavy product visualizations, notification prompts.
- When adding capabilities like camera, microphone, notifications, or GPU access, treat the permission prompt as one control, not the whole defense; the source shows a clickjacking case where a camera turned on with no visible prompt because an invisible window sat under the user's cursor.
- Review each requested capability against whether the store actually needs it; fewer low-level APIs means fewer combinations that can be abused.
- Recognize combinatorial risk: the source notes that as APIs multiply, the number of ways to combine them grows, and each interaction is a potential bug.
- For any UI that requests permission or performs a sensitive action, ensure the visible UI is what actually receives the click (see anti-clickjacking card).
- Log and monitor use of powerful capabilities on customer-facing pages.
Caveat: The clickjacking example is a historical classroom demonstration; specific browser behaviors and available APIs change, so verify current permission models.
Caveat: A permission dialog is not a guarantee the action is safe — it only records that a user clicked something.

Tags: bot-and-agent-security, clickjacking, permissions, third-party-scripts, storefront-security, privacy
Source: Site Security (1).docx

---

## Protect against clickjacking where invisible frames harvest shopper clicks
Use when: Hardening checkout, account, payment, or any one-click action page against having its buttons activated from another site.
- Understand the attack from the source: the user believes they're clicking a game button under their cursor, while an invisible window positioned beneath it receives the click — used to trigger actions (the demo enabled a camera) without any visible prompt.
- Prevent your sensitive pages from being embedded in other sites' frames, so an overlaying attacker page cannot position your real buttons under the user's cursor.
- For high-value actions like placing an order, changing payment details, or confirming a transfer, require a step that can't be satisfied by a stray click — re-entry of credentials, an out-of-band confirmation, or a deliberate multi-step confirm.
- Review whether any third party legitimately needs to frame your checkout or account pages; usually the answer is no.
- Test with a controlled page you own rather than attempting to frame someone else's production site.
Caveat: Anti-framing headers/policies and their browser handling change over time — verify current recommended protections rather than relying on remembered specifics.
Caveat: Anti-framing alone won't stop same-origin overlays or malicious extensions; treat it as one layer.

Tags: bot-and-agent-security, clickjacking, checkout, frame-protection, account-security, defense-in-depth
Source: Site Security (1).docx

---

## Encrypt shopper sessions end-to-end; don't limit HTTPS to payment pages
Use when: Assessing your store's transport security, especially login, account, and browsing session cookies handled over shared or public networks.
- Treat cleartext transport as exposing more than card numbers: the source cites Firesheep, a browser plug-in that harvested cleartext cookies on a local network — enough to surface accounts (e.g., Facebook logins) of people in the same room or café.
- Encrypt the whole session, not just checkout: an attacker on the same network can read anything transmitted unencrypted, including session cookies that authenticate the shopper.
- Use the modern expectation that browsers flag non-HTTPS sites as 'not secure'; the source notes this pressure is deliberate to push owners to adopt HTTPS.
- Mark session cookies so they aren't sent in cleartext and aren't readable by scripts, consistent with your current framework's guidance.
- Inspect adoption across every subdomain and third-party integration, since a single unencrypted endpoint can leak session material.
Caveat: The source says we used to assume HTTPS was only needed for sensitive data like card numbers; that assumption is outdated but the specific Firesheep tool and its era are historical.
Caveat: HTTPS alone does not make an app secure — it protects data in transit, not a vulnerable server or a compromised account (see other cards).

Tags: bot-and-agent-security, https, transport-security, session-management, cookies, checkout
Source: Site Security (1).docx

---

## Model why the web is hard to secure and set realistic expectations for store security
Use when: Setting security strategy and expectations for an ecommerce platform — deciding how much risk to accept and where to invest, and explaining tradeoffs to stakeholders.
- Start from the source's core difficulty: the browser runs code from arbitrary, potentially malicious sources on the user's machine without inspecting it, then must prevent harm.
- Account for backward compatibility ('don't break the web'): the source argues browsers won't remove even annoying legacy features because doing so breaks sites, and users blame the browser — so security fixes often must layer on top of old behavior rather than replace it.
- Factor in pressure to expand capabilities (camera, microphone, GPU, low-level APIs) and its cost: more features mean more API combinations and more potential bugs.
- Expect that the web has evolved rather than been designed from first principles, and that the environment is heavily attacked — yet has accumulated security measures that make it reasonably robust. The source quotes engineer Ilya Grigorik: the criticisms are true, yet the web has proven an incredibly robust platform.
- Translate this into practice: aim for secure architecture and layered controls rather than assuming a clean-slate redesign is available.
Caveat: This is a strategic framing, not a set of controls; the source offers no numeric risk targets.
Caveat: Specific browser compatibility behaviors and vendor positions change — verify current policy rather than treating any remembered rule as fixed.

Tags: bot-and-agent-security, strategy, architecture, browser-security, risk-management, defense-in-depth
Source: Site Security (1).docx

---

## Require strong shopper authentication that survives credential sharing
Use when: Designing or hardening customer account login, password reset, and high-value account actions on your store.
- Accept that social engineering is effective, not rare: the source describes attackers calling staff, impersonating employees, and getting credentials read out, and notes technically literate people fall for these attacks too.
- Aim to design systems secure even if a password is disclosed — the source names two-factor authentication as one approach. Apply it to admin and staff accounts at minimum, and consider it for customer accounts holding payment methods or stored value.
- Because users reuse passwords, a leaked credential from another site can be replayed against yours — watch for credential-stuffing patterns and add rate limiting and anomaly detection on login.
- Protect password reset as carefully as login; a weak reset flow can undo strong login controls.
- Layer authentication with authorization: even a correctly authenticated account must still be checked for permission to perform each high-value action (see the request-tampering card).
Caveat: The source mentions two-factor authentication as a direction and references, in passing, a guest lecture about biometrics at GitHub — treat that as an example of ongoing industry work, not a specific recommendation, and verify current options.
Caveat: The source provides no statistics on social-engineering success rates; treat its 'surprisingly effective' characterization as the presenter's assessment.

Tags: bot-and-agent-security, authentication, two-factor, account-security, social-engineering, password-reset
Source: Site Security (1).docx

---

## Reduce shopper tracking exposure and audit third-party page connections
Use when: Auditing your storefront's privacy and third-party footprint — reviewing trackers, pixels, ad/analytics scripts, and what data leaves on page load.
- Use the source's tool concept — a browser extension that watches which domains your browser contacts and highlights the ones you visited directly versus those data was sent to — and apply it to your own store pages to inventory who is contacted when a shopper lands.
- Expect a much larger web than the visible page suggests: the source notes a handful of visited sites resulted in many other domains being contacted, illustrating how pervasive tracking is.
- Classify each contacted domain: necessary for functionality, analytics, advertising, or unknown — then decide whether to remove, self-host, or consent-gate each.
- Keep the privacy goal tied to shopper rights: the source frames protecting users from tracking and building data profiles as one dimension of web security.
- Re-audit after adding tags, pixels, embedded widgets, or checkout extensions, since each addition can introduce new outbound connections.
Caveat: The extension is described as a demonstration tool; browser extension availability and behavior change — verify a current equivalent before relying on it.
Caveat: The source gives no list of compliant tracker categories; consent and disclosure requirements vary by jurisdiction and are not covered here.

Tags: bot-and-agent-security, privacy, third-party-scripts, tracking, storefront-security, customer-data
Source: Site Security (1).docx

---

## Treat powerful browser APIs as capable of being abused against the shopper
Use when: Evaluating which storage and system APIs your storefront scripts use, and assessing risk from embedded or compromised third-party code.
- Note the source's localStorage case: a supposedly 5 MB per-site limit could be worked around because each subdomain gets its own 5 MB, so an attacker spins up many subdomains and iframes to fill the user's storage until the machine runs out of space and crashes.
- Apply the principle, not the exploit: any API with a per-origin quota can be multiplied across origins, and any storage/resource API can be abused to degrade a shopper's device or degrade trust in your site.
- Keep your own pages from making excessive storage or resource demands, and avoid embedding untrusted third-party frames that could do so.
- When a browser API assumes good-faith use of a limit, ask what happens if the limit is bypassed via multiple origins, repeated calls, or nested frames.
- Stay current with browser fixes: the source notes the localStorage issue was eventually fixed in major browsers, highlighting that platform behavior changes over time.
Caveat: The localStorage exhaustion issue is described as historical and since fixed in major browsers — verify current behavior rather than assuming the technique still works.
Caveat: Do not reproduce attacks on systems you don't own; use this as a design-review lens.

Tags: bot-and-agent-security, browser-apis, storage, third-party-scripts, resource-abuse, storefront-security
Source: Site Security (1).docx

---

## Scope and govern good-faith security testing of your store
Use when: Setting up a pentest, bug bounty, or internal security research program for an ecommerce site, or reviewing what staff and contractors are permitted to test.
- Define what is in scope: your own storefront, admin, APIs, and integrations — the source emphasizes don't attack anything that will get you (or the business) in trouble, and explicitly disqualifies findings manufactured by having a friend build an insecure site.
- Require responsible disclosure rules: don't act in ways that destroy systems or delete data, and ask before taking uncertain actions. The source points to a published bug-bounty process as a rough template for ground rules.
- Recognize that a demonstrated attack is not automatically a responsible test: the source's classroom demos (localStorage exhaustion, clickjacking a camera feed) are illustrations, not procedures to run against live sites.
- Set rules for handling sensitive findings — real collected data, credentials, or customer information should be reported through a controlled channel, not circulated.
- Decide how findings map to remediation urgency using a vulnerability-versus-exploit distinction.
Caveat: The source's policy details are specific to a university course and its bug-bounty program; adapt the principles to your own legal and contractual obligations, which are not covered here.
Caveat: Testing that impacts live shopper data or third-party services can create legal and customer-harm exposure; get explicit authorization first.

Tags: bot-and-agent-security, security-testing, bug-bounty, responsible-disclosure, governance, risk-management
Source: Site Security (1).docx

---

## Map DNS resolution to counter store-domain hijacking
Use when: Hardening your storefront domain, or diagnosing why customers report landing on a look-alike checkout or phishing page for your brand, or selecting DNS providers and records.
- Model the resolution chain the browser actually follows: client → recursive resolver → root nameserver → TLD nameserver (e.g. .com) → your domain's authoritative nameserver → IP address. Each hop is an attack surface, because classic DNS queries are plain text.
- Enumerate the hijack points: malware editing a customer's local hosts file, a compromised recursive resolver (often the ISP-supplied one), a compromised router, a hacked authoritative nameserver, or a registrar account takeover. Any of these can return a malicious IP and send shoppers to an attacker-controlled server posing as your store.
- Mitigate on owned systems: lock registrar accounts with strong unique credentials and MFA, restrict who can edit DNS records, and prefer resolvers that support encrypted DNS where available.
- Understand the TLS counter and its limit: HTTPS uses signatures so clients detect the wrong server, but if an attacker answers the domain lookup, a free certificate authority that only verifies domain control can be induced to issue them a valid certificate. Confirm current provider behavior before relying on any specific check.
- Validate defensively: from your own environment verify records and certificates resolve and match expectations; do not attempt to hijack third-party domains to test.
Caveat: Encrypted-DNS support and certificate-issuance rules change; verify current browser and CA behavior rather than assuming a fixed state.
Caveat: HTTPS alone does not guarantee the request reached your real server if the domain lookup was subverted during issuance.

Tags: bot-and-agent-security, dns, checkout, phishing, domain-security, tls, storefront-infrastructure
Source: Site Security (1).docx

---

## HTTPS, integrity and authenticity for storefront trust
Use when: Deciding how to protect checkout pages, login flows and admin panels, or evaluating what HTTPS actually buys you against tampering and impersonation.
- Treat HTTPS as three guarantees: confidentiality, integrity (responses cannot be silently modified without the client detecting it) and authenticity (you are talking to the server holding the certificate's private key).
- Use integrity to reason about injected content: an intermediary that wants to alter your checkout page or inject a crypto-miner script cannot do so undetected if they lack the private key matching the served certificate.
- Use authenticity to reason about impersonation: a wrong-server attack fails because the attacker cannot present a certificate whose private key they control for your domain — this is the core defense against DNS-hijack phishing.
- Do not assume a padlock equals a legitimately-operated store: cheaper CAs verify only that the requester controls the domain, so a hijacked domain can still obtain a valid cert. Combine TLS with registrar hardening and account MFA.
Caveat: Confidentiality, integrity and authenticity are distinct properties; the source stresses they come as a set for HTTPS but each addresses a different threat.
Caveat: Certificate-issuance verification practices vary and change; verify current CA policies.

Tags: bot-and-agent-security, tls, https, checkout, authentication, phishing, account-security
Source: Site Security (1).docx

---

## Encrypt DNS queries to protect customer browsing privacy
Use when: Choosing DNS configuration for your organization or advising on privacy of traffic to and from your store, or evaluating whether ISP DNS behavior affects your customers.
- Recognize the privacy risk: classic DNS queries are plain text, so the recursive resolver — often the ISP — can log and even sell lists of domains a user looked up, including which stores and services they visit.
- Switch to a provider with an explicit privacy policy stating they do not sell DNS queries, as a partial fix. Note that without encryption, an observing ISP can still see queries even if you point them elsewhere.
- Prefer DNS-over-HTTPS (DoH) where it is available, which tunnels queries over an encrypted connection so observers cannot read them. The source notes Firefox made DoH a default and other browsers were testing it, and that OS-level support was limited — verify current support before relying on it.
- Application to the store: enable DoH at the browser/OS or router level where supported so internal admin lookups and vendor tooling traffic are not trivially readable; assess whether your outbound traffic reveals sensitive internal domains.
- Recognize that ISPs sometimes DNS-hijack invalid domains to show ad/search pages; this is a behavior to be aware of, not a control you administer.
Caveat: Configuring DoH at the router leaves traffic on the local network visible; setting it only in the browser covers just that browser.
Caveat: DoH support and default settings change over time; verify the current state of browsers and operating systems.

Tags: bot-and-agent-security, dns, privacy, encryption, dns-over-https, storefront-infrastructure
Source: Site Security (1).docx

---

## Read HTTP request and response structure to audit store traffic
Use when: Debugging storefront requests in dev tools, understanding method/header usage when integrating an API or CDN, or auditing whether sensitive data leaks into URLs.
- Read a request as: a first line naming the method (GET, POST, PUT, DELETE, etc.), the requested path/resource, and the HTTP version (commonly 1.1), followed by key-value headers. HTTP/1.1 is plain text and human-readable; HTTP/2 and 3 are binary and not directly typeable.
- Read a response as: protocol version and a status code with message, followed by headers and the body. Use the status code category to triage: 2xx success, 3xx redirect, 4xx client error, 5xx server error.
- Leverage extensibility: because headers are just keys and values, servers ignore headers they do not understand, so you can add features (caching, range, conditional requests) without a protocol change.
- Account for statelessness: two consecutive requests have no inherent relationship, so anything that looks like state — a login that persists across clicks — is layered on top via mechanisms like cookies, not the base protocol.
- For the store: audit whether cart tokens, session IDs or customer identifiers are placed in URLs (which get logged and shared) versus headers or cookies.
Caveat: HTTP is transport-agnostic (it can run over channels other than TCP), but TCP is the typical transport; do not assume the transport from the protocol version.
Caveat: Later HTTP versions are not human-readable; use tooling to inspect them.

Tags: bot-and-agent-security, http, headers, storefront-infrastructure, debugging, cart
Source: Site Security (1).docx

---

## Use HTTP status codes to drive caching and retry logic
Use when: Tuning caching/CDN rules, redirects and retry behavior for storefront and checkout endpoints, or diagnosing why a cached page or redirect misbehaves.
- For content serving: 200 means success with the full resource; 206 means a partial response to a range request. Range requests let a client fetch a byte offset (e.g. seeking into a video) without downloading the whole file; if a server ignores the range header it falls back to 200 with the whole file, so clients must handle both.
- For redirects: understand the 301 vs 302 difference. A permanent 301 says the resource is permanently moved, so the browser caches it and stops asking — which breaks any feature that should land on a different page each visit (e.g. a 'random page' link). Use 302 (temporary) when the destination can vary.
- For caching: 304 'not modified' supports conditional requests where the browser sends a version (or a since-date) it already holds and the server replies 304 without resending the body when nothing changed, saving bandwidth. If the client does not include that condition, it gets a 200.
- For errors: 4xx means the client's request was wrong (bad URL, no permission) while 5xx means the server erred (uncaught exception) — this distinction tells you whether retrying is worthwhile.
- For proxy/gateway layers: 502 (bad gateway), 503 (service unavailable/overloaded) and 504 (timeout) reflect failures between a proxy and backend servers.
Caveat: Numeric status meanings come from the protocol spec; specific caching durations and validation values are implementation choices, not fixed numbers.
Caveat: A 301 that varies by request will silently break; confirm your redirect choice matches the intended caching behavior.

Tags: bot-and-agent-security, http, caching, status-codes, cdn, redirects, storefront-infrastructure
Source: Site Security (1).docx

---

## HTTP methods and range requests in practice
Use when: Choosing GET vs POST/PUT/DELETE for a storefront or API integration, or implementing video/audio delivery and seeking on product pages.
- Use GET for requests that fetch a resource and POST/PUT/DELETE for operations that change something. The source treats GET as the common default; do not use GET for actions that mutate state (aligning with the general principle that GET requests should be safe and not change data).
- Recognize the request line groups the method, the path (the requested resource name) and the protocol version, then headers follow. In modern dynamic servers the path need not map to a literal file.
- For media on PDPs, rely on range requests: the client asks for a byte offset and the server can respond 206 with just that slice, enabling seeking into a video before the whole file downloads.
- Build clients to tolerate a 200 response when a range was requested, since servers that do not understand the range header return the full file instead of a 206.
Caveat: The source lists common methods and notes others exist; consult the HTTP spec for the authoritative method list and their safety/idempotency properties.
Caveat: Range behavior depends on server/CDN support; test against your actual delivery stack.

Tags: bot-and-agent-security, http, methods, range-requests, media-delivery, api-integration
Source: Site Security (1).docx

---

## Use URL parsing to distinguish commands from user input
Use when: Building or auditing storefront routing, query-parameter handling, search/filter URLs, or debugging why a URL escaped or failed to resolve.
- Decompose a URL into its parts: scheme (protocol), host (server domain), port, path (the requested resource — dynamic today, not necessarily a file), query (key=value pairs starting with ? and separated by &), and fragment (a # anchor scrolling to a labeled point in the page).
- In query strings, disambiguate delimiter vs data: if a key or value must contain an ampersand, it must be escaped; otherwise it will be read as a separator. This escaping is the core of where user input can be confused with structure.
- Treat this confusion — separating the command from user input — as the root issue behind many web attacks; when building search, filters or redirects from user-supplied values, escape and validate so input cannot become structure.
- For prompts longer than the standard fragment behavior: standard fragments only scroll to anchors the page author pre-defined; a newer spec (which the source says was under consideration) allows control-F-style text matching after the hash. Verify current browser support before depending on it.
Caveat: Path may point to a real file or be fully dynamic; do not assume filesystem semantics.
Caveat: The text-matching fragment behavior was described as a proposal, not established; verify current support.

Tags: bot-and-agent-security, url-parsing, input-handling, storefront-infrastructure, routing, search
Source: Site Security (1).docx

---

## Relative vs absolute vs fragment URLs in storefront links
Use when: Building link generation, breadcrumbs, category pagination or deep links so shoppers land on the intended path rather than a 404.
- Full URLs embed the entire address; relative URLs resolve against the current page's location, effectively appending to the current 'folder'.
- Watch the trailing slash: on a page ending in '/2019/October', a relative link to 'September' resolves to '/2019/September' (the last path segment is replaced), but if the current URL ended with a trailing slash the resolution differs — the source stresses the trailing slash matters.
- Absolute URLs beginning with '/' resolve from the site root, replacing the entire path (e.g. a link to '/events' resolves to same-domain.com/events regardless of the current path).
- Fragment URLs append a #fragment to the current URL, scrolling to a matching labeled element on the page — useful for linking to a specific section of a PDP or help page without the author pre-defining an anchor only if the newer matching behavior applies.
- For the store: standardize link generation (root-relative for internal links) so category, CMS and templated links do not accidentally drop or carry a path segment and produce 404s.
Caveat: Relative resolution quirks (especially trailing slashes) are easy to get wrong; test generated links against real nesting levels.
Caveat: The source notes a fragment text-matching enhancement was under development; do not assume universal behavior.

Tags: bot-and-agent-security, urls, navigation, storefront-infrastructure, catalog, seo
Source: Site Security (1).docx

---

## Treat link/style/script tags as the primary attack surface
Use when: Reviewing how your storefront loads CSS, JavaScript, fonts and third-party scripts, or setting a content-security and dependency-review policy.
- Know the loading model: CSS is loaded externally with <link> and inline with <style>; JavaScript is loaded externally via <script src=...> and inline by pasting it inside <script>. The inconsistency (script vs link) is historical.
- Because these tags pull in external and inline code, treat every third-party tag manager, analytics, chat, pixel and hosted font as untrusted code that executes in your storefront's context — this is the surface the source says most attacks use.
- When auditing: enumerate every link/style/script (including inline) on a checkout or account page, and decide which are truly necessary, since each is a potential tampering or data-exfiltration vector.
- Understand that the web cannot break backwards compatibility, so these historical tag decisions persist and you must design controls around them rather than assuming they will change.
Caveat: The source presents these tags as where the class's attacks live; that is a strong emphasis, not a claim that only these tags are ever involved.
Caveat: Specific mitigations (CSP, SRI) are covered in later material; verify current browser support for any control before relying on it.

Tags: bot-and-agent-security, script-tags, third-party-scripts, content-security, storefront-infrastructure, checkout
Source: Site Security (1).docx

---

## Distinguish JS language, DOM and Node APIs when auditing code
Use when: Reviewing storefront script code, blaming or debugging unexpected behavior, or deciding whether code belongs in the browser or a server environment.
- Classify each API you encounter: features built into the language itself (e.g. arrays) come from the JS spec; document/createElement-style calls come from the browser's Document Object Model; file-reading and networking calls belong to Node.js, not the browser.
- Recognize that the browser supplies DOM APIs because the language alone would have no page to manipulate, and the source attributes most 'bad' APIs to the DOM rather than the language.
- For the store: keep browser and server responsibilities distinct — file reads and socket connections belong on the server (Node), never in client-side storefront JavaScript, which should only manipulate the DOM.
- Note that Node.js added scripting-language capabilities the browser language lacked — filesystem, HTTP, DNS, sockets, a module system for requiring code, and binary data support (before which everything was strings, awkward for media). Modern JS has absorbed some of these needs.
Caveat: Node itself is just 'JavaScript on the command line' with added platform APIs; do not confuse Node's APIs with the language spec.
Caveat: The source notes JS was famously created quickly (Brendan Eich, ~10 days) and its flexibility was a deliberate trade-off; this is historical context, not a security control.

Tags: bot-and-agent-security, javascript, node-js, dom, code-review, storefront-infrastructure
Source: Site Security (1).docx

---

## Assume the browser can move and resize windows (pop-up risk)
Use when: Assessing how your storefront handles third-party or user-generated scripts, or explaining unexpected pop-up/window behavior to stakeholders.
- Note the legacy APIs the source flags: window.open opens a new window (the pop-up API), and moveTo/resizeTo let a page reposition and resize a window; the source notes a browser in 2019 could still do this, and students could build demos making a window follow the cursor.
- Treat this as an attack and abuse surface: any script you embed (ads, third-party tags, user-generated content) inherits the page's ability to open pop-ups, which is why script-sourcing policy matters for a storefront.
- Practical storefront action: control which scripts load on checkout and account pages, and treat pop-up/open-window behavior from embedded third parties as something to constrain rather than assume impossible.
- For users, browsers attempt to restrict pop-up behavior in various versions — but do not assume any given trick is blocked; verify current browser behavior rather than trusting a fixed rule.
Caveat: These APIs' actual behavior and trigger restrictions (e.g. requiring a user gesture) vary by browser and change over time; verify the current interface.
Caveat: The source's window-following demo is an educational demonstration, not a description of a storefront attack.

Tags: bot-and-agent-security, browser-apis, pop-ups, third-party-scripts, script-control
Source: Site Security (1).docx

---

## Use range and conditional requests to speed storefront media and content
Use when: Delivering product video/audio and large assets, configuring CDN caching, or debugging repeated full downloads of unchanged pages or images.
- Implement range requests for media: a client requests a byte offset (e.g. seeking mid-video or mid-song) and the server can return a 206 with only that slice, avoiding a full sequential download before playback.
- Handle the fallback: if a server does not understand the range header, it returns 200 with the whole file, so clients must check the status code and adjust (a 200 when a 206 was expected signals a non-range server).
- Implement conditional requests for caching: the browser sends the version (or a since-date) of a resource it holds; the server returns 304 'not modified' without a body if nothing changed, saving bandwidth, or a 200 with fresh content if it changed.
- Confirm the mechanism requires the client to include the condition header each time; without it, the server always returns 200.
Caveat: The source frames 206 as the reason range requests work; specific offsets and caching windows are implementation choices.
Caveat: CDN and server range/conditional support varies; test your actual delivery path.

Tags: bot-and-agent-security, http, caching, range-requests, cdn, media-delivery
Source: Site Security (1).docx

---

## Design for statelessness and layer state deliberately
Use when: Architecting sessions, carts and login persistence, or reasoning about why two requests have no inherent relationship.
- Treat the base protocol as stateless: two consecutive requests have no built-in relationship, so nothing is remembered by default.
- Recognize that anything that appears stateful in a real storefront — persisting login across clicks, a cart that survives navigation — means the service deliberately layered state on top of HTTP (via mechanisms like cookies, covered in later material).
- When adding state for carts or sessions, decide explicitly what is remembered, for how long, and how it is protected, because the base protocol provides none of these guarantees.
- The source notes a server can implement per-visitor behavior (e.g. counting requests) — but that is the application building state, not HTTP holding it.
Caveat: The source defers the actual state mechanism (cookies) to later material; the mechanism's security details are not covered here.
Caveat: Do not assume statelessness means requests are isolated in practice; application-layer state can still couple them.

Tags: bot-and-agent-security, http, sessions, cart, statelessness, cookies
Source: Site Security (1).docx

---

## Handle proxy/gateway failure codes for resilient checkouts
Use when: Operating a storefront behind a load balancer or proxy, setting timeouts and retry policy, or debugging intermittent checkout errors.
- Understand the architecture: a proxy can sit in front of many backend servers so users see one server, and big web services scale this way. Failures between the proxy and backends produce specific gateway codes rather than client or server errors.
- Map the codes: 502 (bad gateway — the backend is down or unreachable), 503 (service unavailable — temporarily down or overloaded), 504 (timeout — the backend took too long).
- Configure the proxy's timeout deliberately: a backend may be online but slow, and the proxy should give up after a bounded time rather than tie up a connection on a never-ending request.
- Use the code distinction for retry logic: because these indicate a backend/transient problem, a retry may succeed, whereas a 4xx indicates a client mistake that should not be blindly retried.
Caveat: The source presents these as examples of proxy failure modes; specific timeout and retry values are configuration choices, not fixed recommendations.
Caveat: Exact behavior depends on your proxy/load balancer; verify its timeout and retry semantics.

Tags: bot-and-agent-security, http, status-codes, proxy, checkout, retries, storefront-infrastructure
Source: Site Security (1).docx

---

## HTTP status codes drive retry and error-handling logic
Use when: Designing error handling for an ecommerce integration (inventory sync, payment webhook, catalog feed) or deciding how storefront client code should react to a failed API call.
- Read the response status code before deciding what to do. A 404 means the resource is not there; retrying the same request will not help, so surface a real error or fix the URL.
- A 500 means the server had an exception. It is reasonable to retry later with backoff because the failure may be transient.
- A 503 service unavailable means the server is temporarily down or overloaded; retry after a delay rather than immediately.
- A timeout means the request took too long; decide based on your store's needs whether to retry, degrade gracefully, or alert.
- A 400 bad request means the client's request was malformed (the source demonstration removes the required Host header and gets a 400) — fix the request, do not retry unchanged.
- Codes exist separately from messages so that machines and humans can branch on a stable, standard signal rather than parse free-text error strings.
- Build retry policy per code: retry transient (5xx, timeout), do not retry deterministic client errors (4xx) until the request is corrected.
Caveat: The specific meaning of any given code should be verified against current HTTP specifications, which can change; the retry advice here is a design heuristic, not a guarantee of the server's behavior.

Tags: bot-and-agent-security, api-integration, error-handling, integrations, reliability, monitoring
Source: Site Security (1).docx

---

## Use the Host header to route multi-tenant or multi-store requests
Use when: Setting up, debugging, or securing a storefront server, reverse proxy, or CDN where multiple domains or brand sites share infrastructure.
- Always include the Host header in request tooling and custom HTTP clients. Most servers will not respond without it.
- Understand that a single IP address commonly hosts many domains (the source notes a server might serve several sites under one IP). Without a Host header, the server may error (400) or return an arbitrary site.
- When writing storefront or integration code that calls backends, pass the intended store's hostname explicitly so requests hit the correct tenant.
- When building or configuring a reverse proxy, use the Host header to route traffic to the correct backend store.
- In security review, treat Host-header handling as a configuration to validate (mis-routing can send one brand's traffic to another); test on your own infrastructure.
Caveat: The source describes this behavior in a general teaching context; exact proxy and server behavior varies by vendor and configuration, so verify against your current platform.

Tags: bot-and-agent-security, infrastructure, host-header, multi-tenant, routing, configuration
Source: Site Security (1).docx

---

## Treat User-Agent as a weak signal, not an access control
Use when: Analyzing storefront traffic, deciding whether to allow or block a bot, or setting up analytics to distinguish search crawlers from scrapers.
- Read the User-Agent to understand who is visiting: search engines identify themselves (e.g., Googlebot), command-line tools send recognizable strings like curl.
- Use this for analytics and monitoring — e.g., seeing which crawlers or startups are hitting your store — rather than for trust decisions.
- Optionally block requests from an obviously abusive user-agent string (the source blocks a scraper called Site Slurper that was downloading an entire site).
- Do not rely on User-Agent as security: attackers fully control the header and can impersonate a legitimate browser or crawler.
- Pair agent-string filtering with other controls (rate limiting, authentication) rather than treating it as sufficient.
Caveat: The source explicitly states User-Agent is not a good defense because clients control it; it is only useful against obvious, lazy visitors. Specific bot user-agent strings change over time and should be verified.

Tags: bot-and-agent-security, traffic-analysis, crawlers, scraping, monitoring, access-control
Source: Site Security (1).docx

---

## Use referer data to see inbound traffic sources
Use when: Analyzing acquisition channels or investigating where traffic to a product or landing page originates.
- Read the Referer request header to learn which page the user was on before requesting your page.
- Use it to measure how many visitors arrive from a given external site and to attribute traffic sources.
- Recognize that the header is historically misspelled as 'referer' in the HTTP standard and is unlikely to be corrected because changing it would break existing code — this reflects the web's strong preference for backward compatibility over cleaning up old decisions.
- Keep in mind the header is client-supplied and can be stripped or spoofed, so treat it as one signal, not a definitive attribution method; supplement with server-side tracking.
- When building analytics for a store, log Referer to help identify which partner, ad, or site drove a visit.
Caveat: Referer is client-controlled and can be absent or falsified; privacy tools and policies may strip it, so do not treat it as authoritative.

Tags: bot-and-agent-security, analytics, attribution, acquisition, request-headers, measurement
Source: Site Security (1).docx

---

## Use request headers for content negotiation and language
Use when: Implementing storefront localization, serving translated product pages, or optimizing response size for faster page loads.
- Read the Accept-Language header to detect a visitor's preferred language and vary the response (the source demo requests Spanish, then Arabic, and gets back localized content).
- Use Accept headers to decide response format — for example return HTML only when the client accepts HTML, and avoid sending a format the client cannot handle.
- Advertise and honor compression: a client can indicate it understands compressed (e.g., gzip) responses, so the server can compress to reduce payload size.
- Control connection and caching behavior with headers (keep connections open for multiple requests for performance; use conditional requests to fetch only if changed since a date).
- Verify your current framework and CDN behavior, since which headers are honored varies by stack.
Caveat: Header names and supported values are version- and vendor-dependent; confirm against current specifications and your platform's documentation.

Tags: bot-and-agent-security, localization, content-negotiation, performance, request-headers, storefront
Source: Site Security (1).docx

---

## Control caching with response headers to avoid stale or wrong content
Use when: Configuring caching for product pages, localized content, or any personalized storefront response served to many visitors.
- Use cache-control to say a response may be cached, or to forbid caching entirely for sensitive or personalized content that must not be saved on the user's machine.
- Use an Expires value to instruct the client to discard a cached copy after a specific date when you know a new version will be published.
- Set the Vary header to list the request headers that affect the response (e.g., language). The client stores those header values with the cached copy and reuses the cache only when the new request's headers match exactly.
- Worked example from the source: if a page is cached under a Spanish Accept-Language setting, a later Arabic request for the same URL must not reuse it — Vary on the language header prevents the wrong-language page being served.
- Apply the same reasoning to any variable that changes the page (locale, device, logged-in state) and treat those as cache-key dimensions.
Caveat: Vary on too many headers degrades cache hit rate; balance correctness against performance. Specific header handling differs across CDNs and frameworks — verify current behavior.

Tags: bot-and-agent-security, caching, cdn, performance, personalization, response-headers, localization
Source: Site Security (1).docx

---

## Serve large files as streams instead of buffering
Use when: Serving large assets (images, videos, downloadable catalogs) from your store's backend or implementing file endpoints.
- Instead of reading an entire file into memory and then sending it, open a read stream and pipe it directly to the response object (the source uses createReadStream piped to the HTTP response).
- This sends bytes across the socket as they are read, so a very large file (the source cites a 1 GB example) does not require holding the whole thing in RAM before responding.
- Use this pattern for any large asset so the first bytes reach the client sooner and memory use stays bounded.
- Watch for the stream lifecycle: in raw-socket demos the connection may stay open after the response because the client never closed it or the server didn't signal connection close; explicitly manage connection close where relevant.
- Verify your framework's current streaming API, since method names and conventions change between versions.
Caveat: The source demonstrates this with Node's file-system streams; the specific API is version-dependent and should be checked against current documentation.

Tags: bot-and-agent-security, performance, streaming, assets, backend, storefront
Source: Site Security (1).docx

---

## Understand a page load as many chained requests
Use when: Diagnosing slow product pages, optimizing page load, or explaining why a storefront makes so many network calls.
- Recognize the full flow: DNS lookup → open a TCP connection to the IP on the web port → send a GET → receive HTML → parse HTML → build the DOM → render → then request missing sub-resources (CSS, JS, images).
- Expect sub-resource responses to potentially generate more requests, repeating until all resources are resolved and the page finishes rendering.
- Use the browser's developer tools Network tab to inspect exactly which request and response headers the browser sends and receives on your store pages.
- Reduce round trips where you can — fewer requests and earlier requests generally improve perceived load time.
- Use this model when auditing a storefront with an agent or performance tool so failures are traced to the right request, not just the page.
Caveat: The exact rendering pipeline varies by browser and is described here in simplified teaching form; measure with current tooling rather than assuming a fixed sequence.

Tags: bot-and-agent-security, performance, page-load, storefront, developer-tools, diagnostics
Source: Site Security (1).docx

---

## Never trust client-controlled cookies for identity or authorization
Use when: Reviewing authentication or session handling for a storefront, admin panel, or customer account system before shipping.
- Recognize the vulnerability: if the server trusts a plain cookie like username=Alice to identify the user, anyone can edit the cookie to username=Bob and be treated as Bob (the source demonstrates this directly).
- Treat all cookie content as attacker-controlled input. Do not use a client-set value as proof of identity or authorization.
- Apply the principle 'you cannot trust the client': users can modify any client-side state and skip the steps your app expects.
- Validate on the server side: check the identity against a server-held session or signed token rather than reading an unverified value.
- Be aware that many real sites have stored important data in cookies this way; audit your own session design for the same flaw.
Caveat: This is about plain, unsigned cookies; the correct fix (signing or server-side sessions) is covered separately. Cookie attributes and same-site rules also matter and should be verified.

Tags: bot-and-agent-security, authentication, sessions, cookies, access-control, vulnerability
Source: Site Security (1).docx

---

## Sign cookies so tampering is detectable
Use when: Designing session cookies for a storefront or agent integration where you need tamper-evident client-held state.
- Understand the primer: a signing scheme has a generator producing a public key and a secret key, a signer that takes the secret key and a value and outputs a tag, and a verifier.
- When the client returns the value, it also returns the tag. The server verifies the value against the tag using the verification key so it can detect whether the value was changed.
- Apply this so the browser can hold, e.g., username=Alice and the server can be confident the value was not edited to username=Bob.
- Keep the secret key server-side; never expose it to the client.
- Distinguish signing from encryption: signing detects tampering, it does not hide the value.
- Verify your framework's current signing API and key management before relying on it.
Caveat: The source gives an introductory overview, not a full crypto recipe; correct implementation details (algorithm choice, key storage, rotation) require current, authoritative documentation.

Tags: bot-and-agent-security, authentication, sessions, cookies, cryptography, tamper-detection
Source: Site Security (1).docx

---

## Clear a cookie by re-sending it with a past expiry
Use when: Implementing logout or session invalidation on a storefront or customer account system.
- To log a user out, send a Set-Cookie with the same cookie name and any value, plus an expiration date in the past (the source uses 1970-01-01).
- The browser sees the past date and deletes the cookie. The source notes there is no built-in clear operation — this expiry trick is the mechanism.
- The cookie name must match exactly for the clear to work; verify the path/scope also matches so the right cookie is removed.
- After clearing, redirect the user back to a sensible page (e.g., home) as the source does.
- Remember that logout is only effective if the server does not also honor a still-valid token elsewhere; invalidate server-side session state where you maintain it.
Caveat: Cookie attributes (path, domain, secure, same-site) affect whether the clear takes effect; verify against current browser behavior.

Tags: bot-and-agent-security, authentication, sessions, cookies, logout, customer-accounts
Source: Site Security (1).docx

---

## Sessions exist because HTTP is stateless
Use when: Designing cart persistence, login persistence, or any storefront feature that must remember state across page loads.
- Understand that HTTP itself is stateless: without a mechanism, the server cannot tell that two requests come from the same user.
- Use a session — a set of data the server keeps about a user across requests — to solve this.
- Implement it by having the server set a cookie the browser returns on subsequent requests; the server matches those requests to the stored session.
- Apply this to real storefront needs: staying logged in while browsing, keeping a shopping cart populated as a visitor moves between pages, and remembering preferences such as dark mode.
- Note the same mechanism is used for cross-site tracking by ad servers; be mindful of privacy expectations and rules when you use cookies for identification.
Caveat: Cookies are the most common session mechanism but not the only one; server-side sessions and tokens have different tradeoffs. Privacy regulations affect cookie use and should be checked.

Tags: bot-and-agent-security, sessions, cookies, cart, retention, customer-accounts
Source: Site Security (1).docx

---

## Recognize ambient authority and its limits
Use when: Deciding how much access a logged-in customer or an automated agent gets without re-authenticating each action.
- Understand ambient authority: access control is based on a global, persistent property of the requester (the cookie sent on every request), so the user is not re-proving identity every time.
- This convenience is why you stay logged in while browsing and why a like button doesn't require re-entering a password each time; the alternative (re-authenticating every action) is impractical.
- Accept the tradeoff: because the cookie carries the authority, protecting it becomes critical — anyone who obtains or forges the cookie inherits that authority.
- Scope authority narrowly so a stolen or misused credential grants the least access needed, and combine with signing and expiration.
- Note the alternative ambient-authority mechanisms exist (IP-based, built-in HTTP auth), but cookies are by far the most common on the web.
Caveat: Ambient authority is inherently broad; the source treats cookies as the dominant web mechanism but notes IP-based and HTTP-auth approaches exist and are used in narrower cases.

Tags: bot-and-agent-security, authentication, sessions, access-control, cookies, authorization
Source: Site Security (1).docx

---

## Use built-in HTTP authentication and IP checks only in narrow cases
Use when: Evaluating whether to use IP allow-listing (e.g., for an internal admin tool) or deciding against built-in browser auth for customer login.
- IP-based authentication grants access based on the source IP of the request (the source cites libraries allowing access only from campus).
- Recognize its weakness: it can be bypassed if a user routes traffic through a machine in the allowed range, and it is hard to make reliable because TCP connections involve a round trip.
- Understand built-in HTTP authentication as the old browser username/password prompt: it was envisioned as the original web login but is inflexible in UI and experience, so cookies became the norm.
- For a customer-facing storefront, prefer cookie-based sessions with proper signing; reserve IP checks for tightly controlled internal or partner access.
- Verify current browser and platform behavior before depending on any of these.
Caveat: The source marks built-in HTTP auth and some IP-based approaches as rarely appropriate; specifics vary by environment and should be validated.

Tags: bot-and-agent-security, authentication, ip-allowlist, access-control, sessions, infrastructure
Source: Site Security (1).docx

---

## Parse form bodies and cookies with framework middleware
Use when: Building a storefront login, checkout form handler, or any endpoint that receives posted form data or reads cookies.
- Raw form submissions arrive as URL-encoded key/value text (e.g., username=Alice&password=...), which is tedious to parse by hand.
- Add a body parser middleware so the request exposes a clean body object with the submitted keys and values (the source parses username and password).
- Add a cookie parser middleware so requests expose a cookies object with all cookies on the request, instead of parsing the Cookie header yourself.
- Use these parsed values in your route logic to compare credentials or read session state.
- Verify the current middleware package names and setup, since these libraries and their APIs change over time.
Caveat: The source uses specific npm packages during a live demo; the exact module names and usage should be confirmed against current documentation.

Tags: bot-and-agent-security, backend, forms, cookies, middleware, storefront
Source: Site Security (1).docx

---

## Routes and request/response objects structure a storefront backend
Use when: Implementing storefront endpoints such as login, logout, product pages, or cart actions.
- Create a server and have it listen on a chosen port; that makes it an HTTP server.
- Define routes as conditional handlers: when the request method and URL match (e.g., POST /login), run the associated function.
- Match the method correctly — a login form submits via POST, so the route must be POST, not GET.
- Read inputs from the request object (body, headers, cookies) and write outputs through the response object.
- Use a development auto-restart tool so the server picks up file changes, speeding iteration on store features.
- Verify current framework APIs, since these evolve.
Caveat: The source demonstrates with Express and nodemon in a teaching context; API details are version-specific.

Tags: bot-and-agent-security, backend, storefront, routing, development-workflow, http
Source: Site Security (1).docx

---

## Session tokens need server-side revocation, not just signatures
Use when: Designing or auditing how logged-in customers stay logged in — login, logout, 'log out of all devices', and admin account sessions for your storefront.
- Recognize the failure mode: a stateless signed cookie or signed session ID remains valid forever because the server holds no record to delete. A stolen cookie keeps working even after the customer logs out and changes their password.
- Issue a random session ID instead of a signed self-contained token when you need revocability. On login, generate the ID and store a mapping from session ID to user (plus anything else you want to track) in server-side storage such as a sessions table or cache.
- On each request, look the presented session ID up in that store. If it's missing or unrecognized, treat the visitor as logged out.
- On logout, delete that session ID entry from the store. Now the cookie the browser holds no longer matches anything, so it can't be reused.
- Store more than a user name in the session record if useful — the mapping can hold an object of arbitrary complexity for real systems.
- Enable a 'your active sessions' page by listing the customer's stored sessions and letting them delete individual entries, which supports remotely killing a session left open on a shared or friend's device.
Caveat: If malware is persistently on the customer's device watching everything, even revocable sessions can't help — that is out of scope for this defense.
Caveat: The source presents signing as wrong for session identity specifically, not as useless generally.

Tags: bot-and-agent-security, authentication, session-management, logout, cookies, account-security
Source: Site Security (1).docx

---

## Session IDs must come from a large cryptographic random space
Use when: Implementing how your store generates session identifiers for customer or admin logins.
- Never use sequential counters or low-entropy values for session IDs. If IDs run 0, 1, 2..., an attacker who is issued a low number can simply try nearby values and land in another customer's session.
- Generate session IDs from a cryptographically secure random source. In Node, use the crypto module's randomBytes with 16 bytes (128 bits of entropy) and convert the buffer to a string, because cookie values are strings.
- Sanity-check by logging in as two different users and confirming the IDs look completely unrelated.
- Accept that collision between two randomly generated 128-bit IDs is not a realistic concern, so you don't need elaborate collision handling.
- Note the caveat that signing the session ID also blocks guessing, but the source treats signing as a detour here — the simpler fix is a sufficiently large random space plus server-side storage.
Caveat: If session IDs are never stored server-side, even strong randomness doesn't give you logout revocation.
Caveat: Reusing keys across different algorithms or purposes is discouraged — signing is presented as unsuitable for sessions, not as a general pattern to reuse.

Tags: bot-and-agent-security, authentication, session-management, cookies, randomness, account-security
Source: Site Security (1).docx

---

## Use signed cookies only for values users must not alter
Use when: Deciding whether a value stored in a customer's browser cookie may be trusted by your store — e.g. a promotional discount, a cart attribute, or a preference.
- Understand what signing gives you: correctness means a valid value always verifies; security means an attacker who fabricates a value or tag can essentially never pass verification. The signature is not secret — the client can read it — but it prevents modification.
- Apply signing when the client knowing the value is fine but changing it is not. Example from the source: set discount=20 in a cookie and sign it, so the server can confirm the customer didn't edit their browser to discount=100.
- Reject altering the value: if the customer or their tooling changes the signed value or the tag, verification fails and you should not honor the discount.
- Note that signing does not stop sharing — if someone forwards the whole signed cookie to a friend, the friend gets the same discount. The source suggests possibly embedding the user name in the signed blob to bind it, with caveats.
- Do not use signing as the mechanism for session identity, because a signed token can't be destroyed and logout can't invalidate it.
Caveat: Signing hides nothing; the value stays readable in the browser.
Caveat: Signed values remain valid indefinitely — combine signed cookies with server-side records when revocation matters.
Caveat: Framework shortcuts exist (e.g. Express cookie signing via a secret string plus signed-cookie parsing) but the mechanics still reduce to generate keypair, sign, verify.

Tags: bot-and-agent-security, cookies, signing, cryptography, cart, promotions
Source: Site Security (1).docx

---

## Crawl your own checkout flow for third-party script exposure
Use when: Reviewing which tags, pixels, analytics tools, chat widgets, and third-party scripts run on your storefront's logged-in pages and checkout flow.
- Map every third-party script loaded on pages where a logged-in session cookie exists — marketing pixels, chat, analytics, A/B tools. Any of them can read document.cookie in that page context.
- Test directly: in your own browser's dev tools on your site, open the console and evaluate document.cookie while logged in. Whatever the script could see, an attacker who lands script on the page could also see.
- Remember the source's demonstration: an injected image whose src points at an attacker's URL fires a request that carries the cookie, exfiltrating it. Treat any script-reading capability as equivalent to exfiltration capability.
- If a cookie only needs to be sent back to the server (session, auth), add the HttpOnly attribute when setting it so document.cookie can't read it.
- Don't use HttpOnly on values your own front-end script must read (e.g. a theme preference) — those are typically not sensitive and don't belong in cookies anyway.
- HTTPS prevents the on-path sniffing variant of session hijacking; it does not prevent script-based exfiltration, so do both.
Caveat: Historically, unencrypted (HTTP) requests exposed session IDs to anyone watching traffic; a 2010 Firefox monitor-mode extension demonstrated collecting cookies from open Wi-Fi. Treat HTTPS-everywhere as the modern baseline.
Caveat: HttpOnly does not defend against a server that itself is compromised or against other server-side leaks.
Caveat: Older 'Path' scoping is a lie: pages under a different path on the same host can reach a cookie if they run code you can reach with same-origin DOM access.

Tags: bot-and-agent-security, cookies, checkout, third-party-scripts, https, http-only, session-hijacking
Source: Site Security (1).docx

---

## Prefer HTTPS and the Secure cookie attribute for every storefront request
Use when: Configuring transport security and cookie attributes for your storefront, especially login and any page where a customer is authenticated.
- Serve the whole site over HTTPS, not just the login POST. The source's contrast is instructive: the old pattern encrypted only the password submission, then returned an unencrypted session ID used on all subsequent requests — making the session ID the weak point.
- When a site still has mixed HTTP/HTTPS pages (deductible in legacy stacks), mark cookies with the Secure attribute so the browser refuses to send them over unencrypted connections. That means the cookie isn't leaked in the clear; the customer is simply treated as logged out on the insecure page.
- Treat HTTPS-everywhere as the real remedy and Secure/EOL HTTP pages as transitional mitigation.
- Recognize the failure case the source describes: an attacker on the same network grabs the session ID from plaintext traffic, replays it to the server, and is served the private page as though they were the customer. No amount of good session ID generation prevents this if the token travels in the clear.
Caveat: HTTPS does not protect against script-based cookie theft or the cookie's odd same-origin behavior — those need HttpOnly and careful isolation.
Caveat: Modern browsers increasingly force HTTPS; verify current behavior before relying on mixed-mode assumptions.

Tags: bot-and-agent-security, https, cookies, transport-security, session-hijacking, checkout
Source: Site Security (1).docx

---

## Scope cookies with Domain and consider subdomain isolation for your store
Use when: Deciding whether login sessions on your shop subdomain should be visible to other hosts you control (blog, help center, marketing site).
- Understand the default: a cookie set by login.yourshop.com is limited to that subdomain unless you add Domain= yourshop.com, which broadens it to all subdomains.
- Only set Domain when you genuinely need the cookie across hosts — for example a shared login across shop and support subdomains.
- For isolation, rely on the same-origin triple the source describes: protocol + host name + port. Different subdomains count as different hosts, so separate hosts do not automatically share access.
- A practical pattern the source notes: use a distinct subdomain to isolate a component that you don't want sharing cookies with the rest of the site.
- Re-examine third-party or legacy integrations that set Domain broadly — that widens the blast radius of any script-based cookie theft.
Caveat: Never widen scope without understanding what other services share that subdomain.
Caveat: Host-based isolation depends on all your hosts being served as separate origins (protocol/host/port differ), so don't accidentally flatten them.

Tags: bot-and-agent-security, cookies, domain-scoping, subdomains, same-origin-policy, session-management
Source: Site Security (1).docx

---

## Treat cookie Path as broken and design defenses without it
Use when: Evaluating whether path-scoped cookies protect a store's admin panel, embedded login, or a differently-scoped part of a site.
- Know what Path is intended to do: set Path=/blog so a cookie is only sent on requests whose URL begins with /blog, keeping it out of the rest of the site.
- Recognize the established failure: if an attacker can reach the other path's DOM, they can read the cookie even though it was meant to be isolated. The source's visual demonstration: on a different site under the same web host, construct an iframe pointing to the target path, append it (optionally hidden), access iframe.contentDocument, and read document.cookie — because the same-origin policy allowed it.
- Do not treat Path as a security boundary.
- Use genuinely isolating structure instead — separate hosts/subdomains, HttpOnly cookies for server-only values, and server-side session records — rather than URL subtleties.
Caveat: The demo worked because the two paths shared protocol, host, and port — if protocol/host/port differ, same-origin DOM access is denied.
Caveat: This is the source's argument that cookies behave differently from the rest of the web's security model.

Tags: bot-and-agent-security, cookies, same-origin-policy, iframe, path-scoping, isolation
Source: Site Security (1).docx

---

## Don't rely on browser session cookies to expire on close
Use when: Configuring how long a customer's login or cart cookie should persist on your storefront.
- Recognize the gap: a cookie without an Expires date is only supposed to last until the browser session ends, but browsers added session-restoration behavior that often preserves these cookies after closing and reopening.
- If you actually want a cookie to clear, set an explicit expiry date rather than trusting browser-close semantics.
- Avoid far-future expiry dates for session cookies — the source notes Google once set cookies to 2038 and later moved to about two years, but you don't need to be aggressive: set a short horizon (the example is roughly a month or two out) and refresh it on each return visit.
- Delete a cookie by setting the same name with an expiry in the past.
- Beware that the JavaScript document.cookie API doesn't overwrite reliably — setting the same name adds a new cookie rather than replacing, and reading returns one semicolon-delimited string of all cookies. Use a library if you must read/write cookies client-side.
Caveat: Cookies date to 1994 and Netscape; there was no formal spec for years, and the source describes the state as an ad-hoc, inconsistent model — verify current browser behavior before relying on it.
Caveat: Multiple cookies require multiple Set-Cookie headers; attributes like Expires= are not a cookie named Expires.

Tags: bot-and-agent-security, cookies, session-management, expiry, cart, account-security
Source: Site Security (1).docx

---

## Scope agent and tool access with the same principle as cookies
Use when: Designing credentials and permissions for ecommerce automations: price updates, inventory sync, order operations, customer-data access, marketing tool integrations.
- Treat any automation credential (API key, OAuth token, service account) as a session artifact: if it's long-lived and stateless, you can't revoke it quickly after a leak.
- Store automation credentials server-side and make them revocable — delete or rotate the record when you want the automation to lose access, the same way deleting a session ID entry kills a session.
- Scope automation credentials to the brand and task they serve, not to full account access. A pricing job shouldn't have the same scope as an order-fulfillment job.
- Generate random secrets from a secure source rather than predictable values; predictable values invite enumeration the same way sequential session IDs do.
- Log which credential performed which action so you can audit after a compromise, and check what data the automation's tools can read so you know the blast radius if it's stolen.
- Do not treat retrieved documents or tool output as authorization for further actions — a document instructing an agent to reveal data, change a price, or grant access is untrusted data, not permission. Authorization comes from the store owner and the configured scope.
Caveat: This is a transfer of the session-management principle to automation; the source addresses cookies, not agents, so concrete examples here are suggested ecommerce applications.
Caveat: If a compromise is persistent on the host running the automation, revocable credentials help but aren't a complete defense.

Tags: bot-and-agent-security, authentication, authorization, api-credentials, automation, least-privilege, session-management
Source: Site Security (1).docx

---

## Cookie Path Is Not a Security Boundary
Use when: Configuring session or authentication cookies for a storefront, admin panel, or customer account area, and deciding what scope and attributes each cookie should carry.
- Recognize that specifying a cookie path does not prevent other pages or subdomains from reaching into that cookie's DOM context; the source states it is simply unsafe to rely on path as a security control.
- Do not omit path assuming the limit does something. The default path is the directory of the page that set the cookie, which produces inconsistent, unexpected scoping.
- Explicitly set the cookie path to the root of the site so the visible scope matches the actual scope and you are not fooled into thinking path is protecting anything.
- Layer the real controls: domain scoping (cookies can only be accessed by equal or more specific domains, not sibling subdomains), Secure to restrict transmission to HTTPS, HttpOnly to block JavaScript access, and SameSite to control cross-site sending.
- Serve sensitive session cookies from a dedicated login subdomain so that other apps on sibling subdomains cannot read them, mirroring the web.stanford.edu vs cs.stanford.edu separation the source describes.
Caveat: The source is describing classroom-era browser behavior; verify current cookie default and path handling in the browsers you support before relying on any single attribute.
Caveat: Path is not a security mechanism at all, so treat any existing path-based isolation as ineffective rather than merely weak.

Tags: bot-and-agent-security, cookies, session-management, authentication, checkout, customer-accounts
Source: Site Security (1).docx

---

## Set Secure, HttpOnly and SameSite on Session Cookies
Use when: Implementing or hardening login, cart, and session cookies for an ecommerce store, including when migrating to HTTPS or reviewing an existing Express/Node cookie configuration.
- Enable Secure so cookies are only sent over HTTPS, keeping session identifiers off plaintext connections where they could be observed.
- Enable HttpOnly so page JavaScript cannot read the cookie; the browser still stores it and sends it on HTTP requests to the server, which defends against script injected into the page.
- Enable SameSite=Lax so the cookie is not attached to sub-resource requests (embedded images, cross-site form posts) while still being sent on normal top-level navigations. The source calls Lax the best setting for the average site.
- Set Max-Age explicitly (the source used 30 days expressed as 30*24*60*60*1000 milliseconds) and refresh the cookie each time the user returns so the window resets rather than expiring mid-session.
- When clearing a cookie, send the same cookie name with the same attributes (HttpOnly, SameSite, path, domain) and an expiry in the past; otherwise the browser treats it as a different cookie and the original remains.
Caveat: SameSite=Strict is more aggressive and drops cookies even on top-level links from other sites, so users clicking a link from an email or blog may appear logged out; the source calls this probably too aggressive for the average site but plausible for finance.
Caveat: SameSite=Lax breaks legitimate embedding use cases such as third-party comment widgets and ad tracking; the source notes Google has proposed defaulting to Lax and requiring Secure on SameSite=None cookies.
Caveat: In the source's live demo, SameSite did not take effect while the attacker used a raw localhost IP; it behaved correctly once the attacker site used a real-looking hostname, indicating hostname versus IP matters for cross-site classification.

Tags: bot-and-agent-security, cookies, session-management, authentication, checkout, customer-accounts
Source: Site Security (1).docx

---

## Convert Cookie Exfiltration to a Defensive Recognition Checklist
Use when: Reviewing state-changing storefront or admin endpoints (cart mutations, order creation, address or email changes, refunds, password reset) for cross-site request exposure.
- Note the source's key threat: a browser automatically attaches cookies to any request matching the cookie's domain, regardless of which page initiated the request, so a request can carry the user's authority without the user intending it.
- Identify which of your endpoints change state using only cookie-based authentication and no per-request secret. These are the candidates for abuse.
- Understand the classic cross-site request forgery pattern the source demonstrates: a hidden form on an unrelated page posts to your transfer/checkout endpoint, the browser attaches the victim's session cookie, and the server processes it as a legitimate user action.
- Recognize that the source's demo worked even though the request used POST, and worked with the form hidden inside an iframe with a prefilled recipient and amount so the victim never sees it and is not navigated away.
- Treat your own ecommerce state-changing endpoints the same way: if a cross-site page can make the browser submit a valid form with the victim's cookies, the endpoint is exploitable. Apply defense in depth rather than assuming POST alone is protection.
Caveat: The source explicitly states that switching to POST does not stop the attack; forms can be submitted cross-site, which the presenter calls a legacy exception that flies in the face of the same-origin policy.
Caveat: The severity scales with the privilege of the logged-in user: the source notes that hijacking an admin session can allow creating new admin users or running server-side commands, so weight admin endpoints accordingly.

Tags: bot-and-agent-security, csrf, ambient-authority, form-submission, checkout, admin-panel
Source: Site Security (1).docx

---

## Prefer Tokens Over Ambient Cookie Authority for State Changes
Use when: Designing defensive controls for high-value ecommerce operations such as placing orders, changing stored payment methods, issuing refunds, or editing admin permissions.
- Accept the source's framing: ambient authority from cookies is convenient because every request is automatically authorized, but that same automatic behavior is what enables unwanted cross-site actions.
- For sensitive endpoints, do not allow authorization to rest on cookies alone. Require an additional value that a cross-site attacker cannot predict or obtain, in the spirit of the CSRF defense the source promises to cover later.
- Verify the request's origin context rather than trusting that a valid session cookie means the user intended the request.
- Prefer moving the most dangerous operations to server-rendered flows or out-of-band confirmation, and scope authority narrowly so a hijacked session cannot reach operations beyond the task at hand.
- Keep the browser's SameSite behavior as one layer, but the source cautions it is not a complete solution, so do not treat it as the only control.
Caveat: The source does not provide a full CSRF token recipe in this section; it explicitly notes SameSite is one defense that is not a complete solution and defers the rest.
Caveat: The source's demo defense appeared to work once the attacker used a hostname rather than a raw IP, so test your specific deployment rather than assuming the browser will classify your attacker surface as cross-site.

Tags: bot-and-agent-security, csrf, ambient-authority, session-management, checkout, admin-panel
Source: Site Security (1).docx

---

## SameSite Lax versus Strict: Choose by Funnel Impact
Use when: Deciding the SameSite setting for storefront session cookies when your site relies on embedded widgets, affiliate links, email campaign links, or third-party checkout embeds.
- Use the source's definitions: None always attaches cookies; Lax blocks cookies on sub-resource requests from other sites but sends them on top-level navigations; Strict never sends cookies to a site the user arrived at from elsewhere, including top-level navigations.
- For a typical store with email and affiliate traffic, prefer Lax: a user clicking a link from your campaign email should arrive logged in, while hidden cross-site form posts and embedded sub-resource requests should not carry the session cookie.
- Reserve Strict for high-assurance contexts such as finance or admin consoles, accepting that a user clicking a link from an external blog or social post will land logged out in that tab even though they are logged in elsewhere.
- Audit what breaks under Lax: the source's examples are third-party comment widgets that appear logged out and ad-tracking cookies that want to attach to every request; enumerate your own embeds before switching.
- Plan for defaults to change: the source cites a Google proposal to make Lax the default and require Secure on explicit SameSite=None cookies, so review cookie configuration before relying on legacy None behavior.
Caveat: The source calls Strict almost too aggressive for the average site and notes it can confuse users who are logged in elsewhere but appear logged out after clicking a link.
Caveat: The source's demo defense appeared to work once the attacker used a hostname rather than a raw IP, so test your specific deployment rather than assuming the browser will classify your attacker surface as cross-site.

Tags: bot-and-agent-security, cookies, samesite, checkout, customer-accounts, retention
Source: Site Security (1).docx

---

## Why Cross-Site POSTs Still Reach Your Endpoints
Use when: Assessing whether a hidden cross-site form could trigger a state change on your order, account, or admin endpoints even though modern fetch requests would be blocked.
- Classify your request paths: fetch/XHR calls are governed by the same-origin policy and a cross-site caller cannot read the response, but a plain HTML form submission from another origin is still allowed to reach your server.
- For each state-changing endpoint reachable by a simple form post (no custom headers, standard content types), assume a hidden cross-site form can reach it with the victim's cookies attached.
- Do not rely on the attacker being unable to read the response. The source stresses that the damage is done when the server processes the request; the attacker does not need to see the result.
- Reduce the exposed surface by requiring values a cross-site form cannot supply, by verifying origin context, and by keeping privileged operations off simple form-reachable routes.
- Note the source's observation that many sites still use plain HTML forms with JavaScript interception for better UX; the plain-form fallback is what keeps this legacy hole open.
Caveat: The source describes this as a backwards-compatibility exception nobody wanted to break, not an intentional feature; it may change in future browser behavior, so verify current handling.
Caveat: The source's demo defense appeared to work once the attacker used a hostname rather than a raw IP, so test your specific deployment rather than assuming the browser will classify your attacker surface as cross-site.

Tags: bot-and-agent-security, same-origin-policy, form-submission, csrf, checkout, admin-panel
Source: Site Security (1).docx

---

## Same-Origin Policy: What It Allows, Blocks and Leaves Open
Use when: Reviewing storefront widgets, embeds, iframes, third-party scripts, and CDN resource references to understand what cross-origin behavior is expected and what would be a vulnerability.
- Define an origin as the tuple of protocol, hostname and port. If any component differs, the two pages are different origins; the browser enforces this consistently and the source notes it is implemented reliably across browsers.
- Blocked by policy: reading another origin's response body via fetch (the source shows the CORS error and explains the browser refuses to hand back the result because cookies would be attached), and reaching into an embedded document (contentDocument returns null).
- Allowed despite being cross-origin: linking from one site to another, embedding another site in an iframe, navigating an embedded frame to a new destination, and embedding resources such as images or shared JavaScript from a CDN.
- Watch for gaps the source flags: form submissions cross origins (which is how the CSRF attack worked), and cookies use a looser domain-only notion of scope than the same-origin policy, which is why the two rules diverge.
- When you add a third-party embedded widget or shared CDN script, note that you are deliberately granting a cross-origin resource a position in your page; there is no same-origin protection inside that relationship.
Caveat: The source notes the policy is sometimes too narrow (login.stanford.edu cannot share with cs.stanford.edu despite related ownership) and sometimes too broad (two sites from different organizations on the same origin are treated as fully trusted).
Caveat: The source warns it is not enforced for legacy features like form submission, so knowing which features are exempt is necessary to know where your site is vulnerable.
Caveat: Historical browser behavior: verify current same-origin and cookie scoping rules rather than assuming the classroom-era behavior still holds.

Tags: bot-and-agent-security, same-origin-policy, embeds, third-party-scripts, checkout, admin-panel
Source: Site Security (1).docx

---

## Replace legacy document.domain relaxation with explicit messaging
Use when: Evaluating whether a legacy storefront, admin subdomain, or partner integration can rely on document.domain to share cookies or DOM access across subdomains.
- Inventory legacy widgets that assign document.domain or depend on sibling-origin DOM access.
- Prefer explicit postMessage communication between named origins.
- Validate sender origin, expected window and message schema; do not accept wildcard trust for sensitive messages.
- Test the migration with actual embedded checkout, account and support flows.
Caveat: The lecture describes historical browser behavior; origin relaxation does not itself change cookie Domain rules.

Tags: bot-and-agent-security, same-origin-policy, document-domain, subdomains, authentication, legacy-integrations
Source: Site Security (1).docx

---

## Attribute a Hijacked Session to the Right Threat Level
Use when: Prioritizing which ecommerce sessions to protect most tightly and where to require re-authentication, extra confirmation, or a second factor.
- For a normal shopper session, the source's example damage is forced actions such as transferring funds, changing an email address, or resetting a password, all performed as the user.
- For an admin session over a store or CMS, the source states the request can be far more damaging: creating a new admin user, and in some cases running shell commands on the server as the server user.
- Rank your own endpoints by blast radius: customer-facing actions versus admin actions like user creation, permission changes, plugin or theme install, and server-side command execution.
- Apply the strictest controls (stronger authentication, re-confirmation, network restrictions, least-privilege admin roles) to the highest-blast-radius operations, and treat admin session cookies as the most sensitive credential in the store.
- Remember the attacker need not read the response; a successful state change is enough, so log and alert on anomalous admin-level state changes rather than only on errors.
Caveat: The source's damage examples come from a classroom bank and WordPress-admin scenario, not from a measured ecommerce incident; treat them as illustrations of blast radius, not benchmarks.
Caveat: The source assumes the attacker knows the target endpoint path and that the victim is logged in; attacks fail if the user is not authenticated, which does not reduce the need to protect active sessions.

Tags: bot-and-agent-security, session-management, admin-panel, privilege, csrf, customer-accounts
Source: Site Security (1).docx

---

## Short Expiry With Rolling Renewal for Session Cookies
Use when: Choosing session and persistent-login cookie lifetimes for a storefront, balancing shopper convenience against the exposure window if a session is compromised.
- Use the source's heuristic of roughly 30 days for a persistent login cookie, refreshed on each visit, so the expiry is 30 days from the most recent activity rather than from first login.
- Refresh the cookie by sending a new Set-Cookie header with the same name and updated Max-Age whenever the returning user makes a request.
- Keep very short lifetimes on sensitive, less convenience-dependent sessions, and reserve the long rolling cookie for ordinary shopper convenience.
- When implementing expiry, express the lifetime in milliseconds and multiply out the days, hours, minutes and seconds consistently; the source writes 30 days as 30*24*60*60*1000.
- Ensure the same attributes are used on renewal and on clearing so the cookie is updated or removed rather than duplicated.
Caveat: The source presents 30 days as a rule of thumb, not a measured optimum; adjust to your own risk tolerance and regulatory requirements.
Caveat: Long-lived rolling sessions widen the window in which a stolen cookie remains valid, so pair them with the other cookie attributes and origin checks.

Tags: bot-and-agent-security, cookies, session-management, retention, customer-accounts, authentication
Source: Site Security (1).docx

---

## Inspect Request Origin with Security Headers During Testing
Use when: Debugging why a SameSite or CSRF defence appears not to work, and confirming whether the browser is classifying a request as same-site or cross-site for your store.
- When a defence such as SameSite appears ineffective, inspect the incoming request headers that browsers and proxies add to describe where the request came from and how it was triggered.
- Reproduce the test with a realistic hostname rather than a raw IP: the source found the attack still succeeded while the attacker site was addressed by localhost IP and the cookie was re-sent, then behaved correctly once the attacker site was addressed by a real hostname mapped to the same machine.
- Note the source's explanation: cookies scope by domain only and ignore IP-versus-hostname distinctions, while the same-origin policy also considers protocol and port, so a same-IP setup can behave differently from a same-host setup.
- Re-run the cross-site scenario after each change to cookie attributes and confirm whether the cookie is actually being attached to the outgoing request, rather than assuming the setting took effect.
- Keep this validation on systems you own, using your own test domains, and do not treat a passing test on one hostname as proof of protection on another.
Caveat: The source's live debugging was inconclusive at the time and the presenter deferred the explanation to a later session, only confirming the fix after switching to a hostname; do not treat the IP-versus-hostname behaviour as universally guaranteed.
Caveat: Verify the current header names and browser interface, since request-origin metadata and browser defaults change over time.

Tags: bot-and-agent-security, same-origin-policy, cookies, measurement, testing, debugging
Source: Site Security (1).docx

---

## Never Use document.domain to Relax Same-Origin Policy
Use when: Auditing storefront or admin front-end code for cross-subdomain communication (e.g. shop.example.com talking to checkout.example.com) and deciding whether document.domain is acceptable.
- Understand the mechanism: pages can opt in to a common registrable domain by setting document.domain, which relaxes the same-origin check for iframes or popups that also opted in. Protocol and port cannot be relaxed, only the host component.
- Recognise the vulnerability condition: once a legitimate subdomain opts in, any other page on that same registrable domain can also opt in and then read or manipulate the first page's content and cookies. On a store, an attacker-controlled or third-party-hosted subdomain or any XSS on any sibling subdomain gains access to the checkout or account subdomain.
- Prefer per-subdomain isolation: keep authentication, checkout and account pages on their own origins and communicate only via postMessage with strict origin checks, or use a shared backend endpoint.
- If document.domain already exists in the codebase, flag it for removal during review and replace the cross-frame access with postMessage, same-origin API calls, or a server-side session check.
- Verify in the current browser's documentation what the current status of document.domain is; behaviour and deprecation plans have changed over time.
Caveat: The source states this is a bad idea and instructs never to use it.
Caveat: Relaxation applies only to the host component; you cannot bridge different protocols or ports this way.

Tags: bot-and-agent-security, same-origin-policy, iframe, code-review, checkout, authentication
Source: Site Security (1).docx

---

## Use postMessage for Cross-Origin Page Communication
Use when: Building or reviewing legitimate cross-origin communication in an ecommerce flow, e.g. a checkout iframe talking to the parent storefront, an embedded payment widget, or a third-party upsell frame.
- From the sender: obtain a handle to the target window (an iframe's contentWindow, or a window you opened), then call targetWindow.postMessage(message, targetOrigin).
- From the receiver: register a listener with addEventListener('message', handler) and update your UI from the event's data.
- The message can be a structured object (arrays, nested properties, even cyclic references) but cannot include functions, DOM nodes or live object instances.
- For very large payloads such as graphics buffers, use transferable objects so ownership moves to the other page without copying, at the cost of losing your reference.
- Avoid the historical workaround of encoding messages into a child iframe's URL fragment and polling location.hash every fraction of a second; it is slow, fragile and only relevant as history.
- Confirm the current API surface in MDN or the browser vendor docs before implementing, as supported options evolve.
Caveat: postMessage only works when at least one page holds a reference to the other, typically via an iframe or a window opened by script.
Caveat: Without origin validation on both ends the channel is open to any page that can obtain a reference.

Tags: bot-and-agent-security, postmessage, iframe, checkout, integrations, web-apis
Source: Site Security (1).docx

---

## Always Specify targetOrigin When Posting Messages
Use when: Reviewing any code on an account page, login helper or checkout frame that posts user data such as a name or session detail to a parent window.
- Identify every postMessage call in store code and its third-party widgets.
- Ensure the call passes an explicit targetOrigin string (e.g. 'https://shop.example.com') rather than '*' or an omitted argument.
- The browser then refuses to deliver the message if the receiving window's origin does not match, which removes the need to hand-roll origin checks that are easy to get wrong.
- If multiple legitimate destinations exist, some APIs accept an array of origins; verify current browser support before relying on it.
- Treat the destination list as a security boundary and update it deliberately when adding new frames or partners.
Caveat: A recipient you correctly trust may still mishandle the data it receives; the source notes that once information is handed to a cooperative but incompetent site, the sender cannot retrieve or revoke it.
Caveat: Trusting a site to handle data responsibly is a business decision, not a technical control.

Tags: bot-and-agent-security, postmessage, data-leakage, iframe, account-pages, code-review
Source: Site Security (1).docx

---

## Validate event.origin on Every Message Listener
Use when: Hardening storefront frames that receive data such as logged-in status, cart contents, coupon codes or shipping details from a parent or sibling origin.
- Locate every addEventListener('message', ...) callback in the storefront and embedded widgets.
- At the top of the handler, compare event.origin against the exact expected origin and return early on mismatch, before reading or acting on event.data.
- Assume the event object does not identify the sender beyond origin, so untrusted sources cannot be distinguished by any other property.
- Consider window references cheap for an attacker: a page can open a popup or new tab and immediately hold a reference, so any window that does not verify the sender is reachable.
- If a frame may navigate between being legitimate and hostile, re-check origin on each message rather than caching trust at setup time.
Caveat: postMessage makes the origin check easy to omit because it is a runtime property, unlike the sender-side targetOrigin parameter which the API can enforce at call time.
Caveat: The source treats failure to validate origin as a real vulnerability class, not merely a nicety.

Tags: bot-and-agent-security, postmessage, origin-validation, cart, pricing, code-review
Source: Site Security (1).docx

---

## Prevent Clickjacking on Checkout and Account Pages
Use when: Reviewing whether a checkout, buy-now, one-click order, subscription cancel or account settings page should refuse to render inside a third-party frame.
- Understand the attack class: the attacker frames your page, positions it with CSS, sets the frame's opacity to zero, and places their own visible button exactly over a sensitive control such as Buy Now. The visitor sees one button and clicks another.
- The framed action executes with the visitor's ambient session, so the usual outcome is whatever would have happened had they clicked normally, including completing a purchase or bid.
- Compare to what reduces risk: blocking framing on sensitive pages, and using SameSite cookies so a cross-site framed request arrives logged out and cannot complete an authenticated action.
- Evaluate whether a clickjacking defence header or frame-ancestors policy is appropriate for the specific pages, and confirm the current syntax and browser behaviour in vendor documentation.
- Note that HTTPS alone does not stop clickjacking; the source says the same attack works over secure connections.
Caveat: Any site that allows itself to be framed is exposed; the source frames this as the site permitting framing, not as a transport problem.
Caveat: SameSite cookies mitigate the authenticated outcome but are described by the source as a complementary fix, not a complete clickjacking solution.

Tags: bot-and-agent-security, clickjacking, checkout, iframe, samesite-cookies, account-pages
Source: Site Security (1).docx

---

## Set SameSite on Session Cookies to Stop Ambient Cross-Site Requests
Use when: Configuring authentication and cart-session cookies so cross-site requests from third-party pages cannot act as the logged-in shopper.
- Recognise the ambient-authority problem: the browser attaches cookies automatically to cross-site requests such as an embedded image or a submitted form, so the receiving server may treat the request as coming from the logged-in user.
- One illustrated case: an attacker page can embed an image URL that maps to the logged-in user's avatar, confirming login status or making a page look more convincing, because the browser supplies the target site's cookies.
- Apply SameSite to session and authentication cookies so they are only attached on requests originating from your own site; the source describes strict and lax modes and notes you should check the slides or current documentation for exact semantics.
- Test the chosen mode against real flows, because stricter settings affect links clicked from external sites, embedded payments and OAuth redirects.
- Treat this as the preferred fix rather than trying to infer identity from the Referer header.
Caveat: The source describes two modes, strict and lax, and refers to details outside the transcript; verify current cookie attribute names and browser behaviour before shipping.
Caveat: A framed request from your own site to your own site is still within scope, so framing your own pages can reintroduce exposure.

Tags: bot-and-agent-security, samesite-cookies, authentication, cart, iframe, cross-site-requests
Source: Site Security (1).docx

---

## Do Not Rely on the Referer Header for Access Control
Use when: Considering blocking requests to product images, downloads, coupon pages or account resources based on where the request appears to come from.
- Note the intent: the browser sends a Referer header telling the server which page generated the request, and some sites use it to reject or vary responses.
- Identify failure mode one: browsers cache responses. If an image or asset was already fetched legitimately, an attacker's later request can be served from the local HTTP cache without contacting your server, so your check never runs.
- Identify failure mode two: sites can opt out of sending the referrer entirely for privacy reasons, for example documents that embed secret URLs. Google Docs is cited as a case where outgoing links deliberately omit or reduce the referrer.
- Identify failure mode three: referrer policy has several levels from full URL, to origin-only, to nothing, and the modern default already strips the referrer on secure-to-insecure downgrades. The linking site chooses this, not you.
- Where caching is unavoidable, the source mentions a cache-varying header as a partial workaround, but presents SameSite cookies as the better answer; confirm current header names before implementing.
Caveat: A site owner cannot prevent another site from linking to them; the source says there is no real answer for that and Referer inspection is only the best available partial tactic.
Caveat: Referrer policy is set by the page containing the link, so an adversarial linker controls whether you receive the header.

Tags: bot-and-agent-security, referer, caching, access-control, privacy, assets
Source: Site Security (1).docx

---

## Treat Referrer Policy Settings as a Store-Level Trade-off
Use when: Setting or reviewing the referrer policy on storefront pages, order confirmations, customer dashboards or shared cart links.
- Enumerate what you lose with each level: no-referrer hides everything from destinations but also blocks you from seeing inbound referral sources for your own analytics.
- Origin-only reference tells a destination that traffic came from your site, which preserves attribution credit, without exposing the specific page path.
- Full-URL reference supports your own flow analysis across your pages but reveals individual page URLs to any destination you link to.
- Consider the sensitive-URL case: if one of your pages is protected only by an unguessable URL, such as an order status or shared wishlist link, a referrer can leak that URL to whatever the customer clicks next.
- Choose a policy that still allows the analytics and partner crediting you genuinely need, and re-check the currently supported policy values in browser documentation because the defaults have changed over time.
Caveat: The source characterises Google Docs' policy as a bundle covering full URL for same-origin and stripping down to origin or nothing across origins; treat that as an illustration of the trade-off rather than a recommendation for stores.
Caveat: Referrer policy is a blunt instrument and cannot be relied on as a security boundary.

Tags: bot-and-agent-security, referer, privacy, analytics, order-confirmation, shared-links
Source: Site Security (1).docx

---

## Treat Cross-Origin Script and Style Embeds as Full Trust
Use when: Deciding whether to load third-party JavaScript, CSS, fonts or pixels on product pages, checkout or account pages.
- List the automatic exceptions to the same-origin policy: pages may embed images, stylesheets, scripts, fonts and other resources from other origins, link to them, and submit forms to them, but cannot read data back from another origin.
- Recognise that an embedded script runs in your page's context, exactly as if you had pasted the code into your page. It can therefore read and act on everything your page can, including form fields and session-dependent behaviour.
- Apply this to tag managers, chat widgets, reviews, A/B testing tools and analytics on checkout: each is a script with full page authority, not a sandboxed component.
- Prefer self-hosting or reviewing critical libraries, and keep third-party scripts off the most sensitive pages where possible.
- Remember that cross-origin stylesheet and font embeds are common and generally lower risk than scripts, since they carry layout and font data rather than executable code.
Caveat: The source notes these embed permissions predate the same-origin policy and were effectively grandfathered in; that is why they feel inconsistent with origin isolation.
Caveat: There are minor edge cases around content-type sniffing that the source declines to cover in detail.

Tags: bot-and-agent-security, third-party-scripts, content-security, checkout, product-page, integrations
Source: Site Security (1).docx

---

## Prevent Cross-Site Script Inclusion Leakage of JSON Endpoints
Use when: Reviewing API or data endpoints on a store that return buyer data, pricing tiers, inventory or account details and may be fetchable as scripts.
- Understand that a script loaded from another origin runs in the loading page's context, so an attacker page can include a script tag pointing at your data endpoint and receive whatever the browser parses as JavaScript.
- When you inspect JSON-returning endpoints in a live store, look for an unusual leading sequence of characters before the data; the source points to such a prefix in a major webmail response as a deliberate defence against this class of inclusion attack.
- Treat a syntactically invalid prefix as the defensive idea: the payload then fails to parse as a script in a foreign page while remaining parseable by a careful legitimate consumer.
- Add an equivalent prefix only together with verifying that existing legit clients still parse the response, and that the endpoint does not leak session-scoped data solely because cookies were attached.
- Pair this with SameSite cookies and origin checks on the endpoint so inclusion alone does not reach authenticated data.
Caveat: The source presents the prefix observation as a motivating puzzle rather than a fully specified recipe; do not copy an exact hard-coded prefix without testing your own parsers.
Caveat: JSON is not generally valid JavaScript in all cases, but the source treats script-compatible responses as the live risk.

Tags: bot-and-agent-security, cross-site-script-inclusion, api-security, json, data-leakage, samesite-cookies
Source: Site Security (1).docx

---

## Do Not Trust Cookie Path Scoping as an Origin Boundary
Use when: Designing cookie scope for a store with several subdomains, such as www, account and checkout, or auditing an existing cookie configuration.
- Note that cookies are more specific than origins in one direction, allowing a path restriction, but that path scoping is ineffective as isolation because pages on the same origin can frame each other and read the sibling's cookies.
- Note that cookies are less specific in the other direction: a page on one subdomain can set cookies for the broader registrable domain, and a DNS-hijacked or otherwise hostile response on that domain can read and set cookies for the whole domain.
- Illustrate the risk with the invalid-domain case: if an ISP hijacks a nonexistent domain and serves an ad page, JavaScript on that page can read and set cookies for that domain, so an insecure or malicious ad is enough to compromise it.
- Choose your session cookie's domain deliberately, prefer host-only cookies where subdomains do not need to share the session, and avoid broadly scoped cookies for authentication.
- Combine with SameSite and HTTPS on the whole site, since the source notes that mandating HTTPS addresses the network-interception leg of this scenario.
Caveat: The source stresses that cookies were designed before the same-origin policy and were never retrofitted to match it.
Caveat: HTTPS fixes interception; it does not by itself fix scoping mistakes or same-domain hostility between subdomains.

Tags: bot-and-agent-security, cookies, same-origin-policy, subdomains, authentication, dns
Source: Site Security (1).docx

---

## Bound Validation of Cross-Origin Flows to Owned Environments
Use when: Prototyping or regression-testing cross-origin communication in a store's checkout or account flow before shipping postMessage or frame changes.
- Reproduce the environment safely: run two local servers on different ports so that the pages count as distinct origins under the origin tuple rule, and load one inside an iframe of the other.
- Instrument what you need to see, for example rendering the received message string into a visible element so you can confirm delivery and timing.
- Verify sender-side enforcement by setting targetOrigin to the exact expected origin and confirming the browser drops messages when the frame points elsewhere.
- Verify receiver-side enforcement by checking event.origin and returning early on mismatch, then attempting a message from a deliberately wrong origin to confirm it is ignored.
- Keep the harness to systems you own or are authorised to test, and never point these techniques at production third-party sites or real customer sessions.
Caveat: The source demonstrates these techniques in a classroom with two local servers; the localhost ports are a teaching setup, not a deployment recommendation.
Caveat: Origin equality includes scheme and port, so a same-host page on a different port is a distinct origin for these checks.

Tags: bot-and-agent-security, postmessage, origin-validation, test-harness, iframe, checkout
Source: Site Security (1).docx

---

## Prevent Clickjacking with Frame-Ancestors Header
Use when: Hardening your storefront or admin dashboard against clickjacking, e.g. when a third party could overlay a hidden add-to-cart or account action over an enticing button.
- Understand the attack: if your site allows framing, an attacker page can embed your site in a full-page iframe and transform/zoom it so a click lands on your real button (e.g. a social like button or an authenticated account action) while the user thinks they clicked something else.
- Serverside, send the frame-ancestors directive in the response: 'none' to forbid all framing, or "'self'" to allow only your own origin to frame you. This is the reliable defense the source recommends over JS frame-busting.
- Set the policy on every page or at the site-wide header level; do not assume you can detect at request time that a request is a framing attempt, since the server often cannot see it.
- Verify on your own staging site by embedding your page in a test iframe and confirming the browser refuses to load it.
- If you must support very old browsers, note the source says this header is long-supported and pervasive, but for other defensive headers check current browser support before relying on them.
Caveat: Legacy X-Frame-Options with ALLOW-FROM is inconsistently supported; prefer frame-ancestors.
Caveat: Frame-busting JavaScript is not a reliable defense per the cited Stanford research on busting frame busting.
Caveat: Recently, browsers correctly require the entire embed chain to be same-origin; older behavior allowed an A->B->A chain. Verify with current browser behavior before relying on edge cases.

Tags: bot-and-agent-security, clickjacking, http-headers, checkout, account-security, storefront-hardening
Source: Site Security (1).docx

---

## Reject Cross-Site Form Submissions Using Origin Header
Use when: Protecting storefront or checkout endpoints that accept form POSTs, such as changing an account email, applying a promo code, or placing an order, from being forged by a third-party page.
- Recognize that SameSite cookies only strip cookies from cross-site requests; they do not prevent the form submission itself, so the POST still arrives.
- Serverside, read the Origin header on incoming POST requests and compare it against an allow list of origins you expect (e.g. your own storefront domain).
- Reject requests whose Origin is missing or not on the allow list.
- Note that GET requests are treated as CORS-simple and may not carry an Origin header for image/script/style loads; rely on the POST check for state-changing actions rather than expecting Origin everywhere.
- Do not rely on the Referer header as a primary control; the source says it can be manipulated and is not reliable.
Caveat: The browser sets and protects the Origin header; a site making the request cannot forge it, which is why it is trustworthy for this check.
Caveat: You cannot truly stop a determined client (e.g. a script) from sending a request; the goal is to make your server reject requests it did not originate.

Tags: bot-and-agent-security, csrf, http-headers, checkout, account-security, origin-header
Source: Site Security (1).docx

---

## Protect private ecommerce media with authorization or scoped links
Use when: Serving images such as user avatars, customer-uploaded photos, downloadable receipts, or paid content where hotlinking or leaking would cost bandwidth or expose private data.
- Classify the asset: public product media, customer upload, invoice or private support attachment.
- Enforce server-side authorization for private assets or issue appropriately scoped, expiring signed links after authorization.
- Treat a shared link as a bearer capability that can leak through logs or forwarding; avoid unnecessary exposure.
- Use caching, rate limits and delivery controls for public-media hotlinking without confusing them with customer-data access control.
Caveat: A random path alone does not establish the requester's identity or permission.

Tags: bot-and-agent-security, hotlinking, image-security, bandwidth, signed-urls, asset-delivery
Source: Site Security (1).docx

---

## Choose the Right Tool for Each Cross-Site Boundary Question
Use when: Architecting storefront integrations, embedded widgets, third-party scripts, or any cross-origin data sharing and needing to know which control actually holds.
- Can site A link to or embed site B? By default yes; block it with the frame-ancestors header if you don't want to be embedded, and the source says this works reliably.
- Can site A embed B and modify B's DOM? No; the same-origin policy is strong here and there is no way to relax it, so this stays a safe default.
- Can a site submit a form to you? You can reject cross-origin submissions by checking the Origin header, which the source says works quite reliably.
- Do you want forms allowed but without cookies attached? Use SameSite cookies for that middle ground.
- Can another site read the bytes of your response? No; strengthening this is not foolproof, and the source treats 'images and scripts' defenses as best-effort only.
- When you need to intentionally allow cross-origin reads (e.g. collaborating with a partner API), plan to relax the policy explicitly rather than weakening defaults.
Caveat: Only the frame-ancestors and Origin-allow-list controls are described as reliable; Referer-based and similar tricks are explicitly not foolproof.
Caveat: Verify current browser behavior for any relaxation mechanism before shipping, since these details change.

Tags: bot-and-agent-security, same-origin-policy, cors, http-headers, integrations, security-architecture
Source: Site Security (1).docx

---

## Kill Cross-Site Scripting by Escaping User Data at Output
Use when: Building any storefront page that reflects user input, such as a search results page, a personalized welcome based on a URL parameter, or a product review display.
- Identify the pattern that causes the bug: server code concatenating a hard-coded HTML template with untrusted user input, so the browser cannot tell the user's string from your markup.
- Understand the impact: an attacker who gets their text parsed as code can run script in your origin's context, taking actions as your logged-in customer (e.g. reading document.cookie and exfiltrating it, or submitting requests).
- Fix it by escaping the untrusted value so angle brackets and other significant characters become inert HTML entities (e.g. < becomes &lt;), so the browser displays the text instead of executing it.
- Escape only the specific values that are user-supplied, not the entire page; escaping everything would turn your own tags into visible text.
- Prefer your web framework's built-in output-escaping for inserting data over hand-rolled functions where possible.
- Do not rely on a blocklist of 'bad words' (like banning usernames containing 'script' or 'select') as your primary defense; per the source, missing a single entry defeats it.
Caveat: The source's example demonstrates this all with a same-tab self-test (alerting your own cookie); a real attack requires the victim to be logged in and to click a link, which is why 'don't click suspicious links' is not sufficient protection.
Caveat: Note the distinction between escaping for HTML text context versus other contexts; the source only demonstrates HTML escaping.

Tags: bot-and-agent-security, xss, input-sanitization, output-escaping, product-page, search, account-security
Source: Site Security (1).docx

---

## Why Cross-Site Scripting Is Worse Than Clickjacking for Your Store
Use when: Prioritizing remediation when you discover a stored or reflected input vulnerability on a customer-facing page like a profile, review, or search results page.
- Recognize that the same-origin policy blocks an attacker from framing your site and reaching into the login form to read a password; XSS is the workaround that gets their code into your page.
- Trace what an attacker can then do: take any action as the customer (submit requests with the victim's cookies), or read document.cookie and send it to an attacker server to hijack the session.
- Treat any page that mixes attacker-controlled text with your code as a potential injection point, whether it is reflected (in a URL parameter) or stored (saved to your database and shown to other users).
- Prioritize fixes for stored injection on pages other customers view, since that enables self-propagating worms (the source's MySpace example added the attacker as a friend and copied the payload into victims' profiles, causing exponential growth and an outage).
- When reviewing your store, test your own pages with a harmless proof payload (e.g. alerting the current document cookie) so you confirm the vulnerability without attacking anyone else.
Caveat: The source stresses that clients cannot be trusted at all; server-side defenses must hold even if a client is a hacked browser or script.
Caveat: Worm-style exponential spread is a described historical case study, not a prediction of outcomes for any specific store.

Tags: bot-and-agent-security, xss, session-hijacking, threat-model, stored-xss, account-security
Source: Site Security (1).docx

---

## Avoid JSONP for Partner Data; Prefer Headers or Proxy
Use when: Deciding how a storefront should read JSON from a partner or internal API that lives on a different origin, especially when the data varies per logged-in user.
- Understand the trick: a script tag bypasses the same-origin policy, and JSONP asks the server to wrap its JSON in a caller-specified function name (callback parameter) so the returned script calls your function with the data.
- Recognize the dangers: the server must write extra code to support it, some valid JSON is not valid JavaScript (whitespace issues), and the caller controls the callback name, which opens a reflected-file-download / injection class of bug if not sanitized.
- From the consuming site's view, including a script from another origin gives that origin remote execution in your page if their response is ever compromised.
- Consider alternatives before adopting JSONP: a serverside proxy on your own domain (which also lets you keep the request authenticated to your own session), or a proper CORS-style header that the other server sends to permit your origin to read the response.
- If you must relax the boundary intentionally, restrict it narrowly rather than granting full script execution.
Caveat: The source describes JSONP as a 'clever hack' that works but is a bad idea for untrusted or unstable partners.
Caveat: A serverside proxy changes where the request originates and won't reflect per-user logged-in responses the way a browser-side call would.

Tags: bot-and-agent-security, jsonp, cors, integrations, script-tags, api-security
Source: Site Security (1).docx

---

## Layer CSRF defenses on authenticated store actions
Use when: Configuring session cookie attributes for a storefront so cross-site pages can't trigger authenticated actions like account changes or a placed order against a logged-in customer.
- Keep state changes out of safe read methods such as GET.
- Use maintained framework CSRF protections and validate the expected token for relevant authenticated actions.
- Validate request origin as appropriate and set Secure, HttpOnly and a suitable SameSite policy on session cookies.
- Test cross-site login, payment redirects and embeds; Lax, Strict and None have different behavior.
- Recognize that same-site sibling origins and XSS can undermine assumptions; keep authorization and output safety independent.
Caveat: SameSite is defense in depth, not a universal guarantee that every cross-origin request is unauthenticated.

Tags: bot-and-agent-security, samesite-cookies, csrf, checkout, account-security, session-management
Source: Site Security (1).docx

---

## Treat Script and Image Inclusion as Best-Effort, Not Secure
Use when: Deciding whether and how to stop other sites embedding your images, stylesheets or JavaScript (e.g. a signature animation or theme asset they are stealing).
- Clarify the goal: for a static image, script or CSS asset, the concern is bandwidth theft (hotlinking), not data leakage, because the asset holds no private data.
- Recognize that a hotlinked script runs in the embedding site's page, not yours, so it does not threaten your origin directly.
- Use Referer-based checks to reduce casual hotlinking, but accept that the source calls this not foolproof because the header can be manipulated.
- For private or per-user assets, prefer unguessable URLs or SameSite-gated responses rather than Referer rules.
- Use a CDN (the source cites Google's CDN serving the d3 graphics library) as normal practice for serving such libraries, separate from the hotlinking question.
Caveat: The source explicitly lists image/script protection as best-effort; do not treat it as a security boundary.
Caveat: Origin headers are not sent for simple image/script/style loads, so an Origin allow list won't cover this case.

Tags: bot-and-agent-security, hotlinking, cdn, referer, bandwidth, asset-delivery
Source: Site Security (1).docx

---

## Make Store Input Fields Untrusted by Default
Use when: Reviewing storefront and back-office features that accept customer text — signup fields, search boxes, review forms, support messages, profile/bio fields — before launch.
- For every place customer data is combined with code, name the code context: HTML output, a SQL command, a URL, or JavaScript.
- Apply the correct neutralization for that context (HTML escaping for HTML, parameterized queries for SQL) rather than one generic sanitizer.
- Prefer frameworks and ORMs that parameterize queries and escape output by default, and confirm they are actually enabled rather than bypassed for convenience.
- When the user's data modifies a SQL command, the risk is reading different data or running a second command — the same class of bug as XSS applied to the database.
- Include stored fields (bios, reviews, display names) in your review, since stored injection can spread to every visitor's page.
Caveat: The source notes the SQL-injection parallel briefly; the detailed lecture focus is XSS.
Caveat: Blacklisting programmer-sounding usernames is called out as an inadequate defense on its own.

Tags: bot-and-agent-security, input-sanitization, xss, sql-injection, account-security, launch-readiness
Source: Site Security (1).docx

---

## Automate Defensive Controls Across All Store Pages
Use when: Rolling out security headers and escaping after an audit reveals inconsistent coverage across your storefront's templates.
- Set frame-ancestors (or the legacy X-Frame-Options header) as a site-wide response header so every page — product, cart, account, admin — refuses untrusted framing.
- Enable your web framework's automatic output escaping by default and audit for places where developers disabled or bypassed it.
- For each reflected input (URL parameters driving page text), confirm the untrusted value is escaped before it reaches the HTML string.
- Add the Origin allow list to your shared POST-handling middleware so new endpoints inherit the check.
- Re-test after rollout with self-directed proof payloads on staging to confirm controls fire on every template.
Caveat: Retrofitting a site-wide header is easy; retrofitting escaping may require touching many templates and finding old bypasses.
Caveat: Verify header and attribute support in the browsers your customers actually use before assuming blanket protection.

Tags: bot-and-agent-security, http-headers, output-escaping, clickjacking, storefront-hardening, framework-security
Source: Site Security (1).docx

---

## Treat all client-supplied data as untrusted input
Use when: Designing or reviewing any storefront feature that echoes user input — search terms, review text, profile names, wishlist labels, coupon codes, or URL parameters — back into the page.
- Assume every value originating from the browser (query string, form field, header, stored profile field) is suspect regardless of how mundane it looks.
- Identify every place that value is inserted into HTML, an attribute, or inline JavaScript — each insertion point needs its own correct escaping.
- Prefer the escaping mechanism built into your framework or templating language (e.g. ejs, Jade) over hand-rolled concatenation of HTML strings with user data.
- Read the framework docs to find the safe insertion helper and the explicitly dangerous opt-out; treat the opt-out as requiring justification, not convenience.
- For high-power attributes (src, href, style, event handlers), do not rely on generic escaping; validate the value separately (see related cards).
- Log where untrusted data enters your stack so future features inherit the same discipline.
Caveat: The source cites research (a WhiteHat Security report circa 2015-2016) that roughly half of sites had XSS issues; this is a historical statistic, not a current benchmark.
Caveat: Framework behaviour and default escaping change over time — verify the current interface and defaults for whatever framework you use.

Tags: bot-and-agent-security, input-validation, output-escaping, pdp, customer-research, checkout
Source: Site Security (1).docx

---

## Escape user data inside HTML element contexts
Use when: Rendering user-supplied text into normal page regions such as review bodies, collection descriptions, order notes, or any block that is not a script, style, comment or tag name.
- Replace left angle brackets (<) with the HTML entity (&lt;) so the browser shows the character instead of starting a tag.
- Also replace ampersands (&) with the entity (&amp;) — otherwise a user typing the literal sequence '&lt;' would be rendered as a real '<' and could re-open an injection.
- For attribute values, additionally convert both single and double quotes to their HTML entities, so it does not matter which quote character surrounds the attribute.
- Do not apply HTML entity escaping to the whole page — that would show every legitimate tag as visible text; only escape the specific untrusted variables.
- Where possible delegate this to your framework's safe-insertion helper, but understand what it does so you can audit it.
Caveat: This rule covers ordinary element text and quoted attribute values only; script and style blocks have completely different rules.
Caveat: Escaping entities inside a script block does not work because the JavaScript parser does not understand HTML entities.
Caveat: Over-escaping is generally harmless to display (any character can be turned into an entity), but it breaks contexts where the parser expects raw characters.

Tags: bot-and-agent-security, output-escaping, html-entities, pdp, input-validation
Source: Site Security (1).docx

---

## Always quote HTML attribute values you build
Use when: Generating HTML snippets for product images, alt text, srcsets, data attributes, or any element whose attribute values include dynamic store data.
- Always wrap dynamic attribute values in quotes in your templates; do not emit attributes like alt=userText with no quotes.
- Recognise that an unquoted value cannot safely contain a space, and browsers also treat many other characters as ending the value, not just spaces.
- Treat unquoted attributes as effectively impossible to escape correctly, because you would need to block a long and browser-dependent list of characters.
- When reviewing templates or generated markup, flag any attribute whose value is unquoted and dynamic.
- Rely on the framework's templating, which quotes attributes for you, rather than manual string concatenation.
Caveat: Historically browsers disagreed on which characters terminated unquoted values; behaviour is more standardised now but still a poor practice.
Caveat: This is defence-in-depth: quoting alone does not make high-power attributes safe.

Tags: bot-and-agent-security, output-escaping, attributes, pdp, input-validation
Source: Site Security (1).docx

---

## High-power attributes need value validation, not just escaping
Use when: Any storefront flow that lets a user or merchant supply a URL for an image, link, iframe, or script — user avatars, custom collection banners, affiliate links, or rich-text product descriptions.
- Do not assume that escaping quotes is sufficient for src or href; even a well-contained value can cause a script to load or a page to navigate somewhere dangerous.
- Validate that the supplied value is a well-formed, expected URL (correct scheme and shape) in addition to quoting and escaping it.
- Explicitly reject the data: and javascript: schemes, which are legitimate URL forms but enable script execution and page injection.
- For iframe or script sources specifically, restrict to trusted origins you control or explicitly allow.
- When writing validation regexes, test them against data: and javascript: payloads, since these are easy to overlook and cause serious outcomes.
Caveat: Data URLs have legitimate uses (see the data-URL card); the risk depends on where the value is inserted.
Caveat: The source notes uncertainty about how some data-URL iframes are treated origin-wise; do not rely on iframe origin isolation without verifying.

Tags: bot-and-agent-security, url-validation, attributes, landing-page, pdp, acquisition
Source: Site Security (1).docx

---

## Reject data: and javascript: URLs in user-supplied links
Use when: Building any feature that accepts a user-submitted link or image source — user-generated content, curated wishlists, third-party product feeds, or rich product description editors.
- Understand that a data: URL is a synthetic response from a non-existent server: the browser pretends to fetch it and treats the contents after the comma as the document.
- Understand that a javascript: URL runs code in the current page; browsers such as Chrome may strip the javascript: prefix on paste, but users can re-add it, so do not rely on that.
- Whitelist accepted schemes for user links (typically https) and reject everything else, rather than blacklisting only the two known-bad schemes.
- For images, restrict to image data URLs or a controlled CDN origin if you must permit them at all.
- Re-test after any change to link handling, and log rejected scheme attempts to spot abuse.
Caveat: Chrome, Firefox and Safari handle pasted javascript: URLs differently (stripping the scheme or requiring a setting), so browser behaviour is not a reliable control.
Caveat: Even if a data-URL iframe is isolated by origin, a heavy or blocking script inside it can still lock up the page in the shared event loop (a denial-of-service concern).

Tags: bot-and-agent-security, url-validation, scheme-allowlist, acquisition, landing-page
Source: Site Security (1).docx

---

## Escaping alone fails inside inline event handlers and JS strings
Use when: Generating trigger text, analytics labels, or inline event handlers that embed store data, or embedding a user string inside a <script> variable.
- Recognise that data inside an onclick or script variable is in a JavaScript context nested inside an HTML context — one layer of escaping is not enough.
- For strings inside JavaScript, escape quotes by prefixing with a backslash, and also escape backslashes themselves, otherwise a supplied backslash can neutralise your escape.
- For values inserted into script variables, consider hex-encoding the data (using only 0-9 and A-F) so it cannot contain quotes, closing script tags or other breakout characters; decode it at runtime.
- Alternatively use the HTML <template> tag as inert storage: put the escaped user data between tags (only < and & need escaping), then read it via JavaScript when needed.
- Write tests with inputs containing quotes, backslashes, closing script tags and mixed contexts.
Caveat: Pure HTML entity escaping inside a script produces garbage because the JavaScript parser has no concept of entities, so the user sees the wrong text.
Caveat: The source notes some edge cases (e.g. double-backslash handling) were uncertain in the lecture — validate against your own parser and runtime.

Tags: bot-and-agent-security, javascript-context, output-escaping, pdp, input-validation
Source: Site Security (1).docx

---

## Avoid pages where user data passes through nested parsers
Use when: Designing features where store data flows through an HTML attribute, then a JavaScript string, then a dynamic execution call (e.g. rich-text widgets, custom button scripts, or analytics configuration).
- Identify nesting when a single value must be escaped at multiple levels — e.g. user data inside a string inside an onclick attribute, which the browser parses as HTML, then as JavaScript, then as a string argument.
- Count the escapes required: each nested context adds its own layer, and getting the order or characters wrong breaks security.
- Prefer architectures that avoid inline scripting and multi-layer embedding: pass data as escaped HTML between tags and read it via a script, rather than rebuilding scripts from strings.
- If you cannot avoid nesting, write explicit tests that inject breakout characters at each layer and confirm nothing escapes.
- Document the escaping contract wherever developers must remember multiple layers.
Caveat: The source describes such nesting as surprisingly common in real code, but its recommended remedy is to avoid it rather than perfect the escaping.
Caveat: No numeric guidance is given; the rule is architectural, not a formula.

Tags: bot-and-agent-security, context-awareness, output-escaping, pdp, experiment-design
Source: Site Security (1).docx

---

## Only HTML element text and quoted attributes are reliably escapable
Use when: Reviewing or designing any template or editor where store or customer data could land in a comment, in a tag name, or directly in a script body.
- Refuse to insert user data into HTML comments — they do not affect rendering, so there is no legitimate need, and the parser rules are difficult to get right.
- Refuse to build tag names from user input; even a blacklist of dangerous tags (script, style) will miss new tags and browser-specific interpretations.
- Never place raw user data in an unquoted script position; use the hex-encoding or template-tag approaches described elsewhere.
- Reserve the escapable contexts — ordinary element text and quoted attribute values — for any user-dependent content.
- When a feature seems to require a non-escapable context, redesign the feature rather than attempting clever escaping.
Caveat: The source states the comment-parsing rules were hard to pin down, which is itself a reason to avoid, not to improvise.
Caveat: Blacklist approaches fail as browsers evolve and add new elements.

Tags: bot-and-agent-security, input-validation, output-escaping, pdp, experiment-design
Source: Site Security (1).docx

---

## Recognise reflected versus stored XSS and prioritise accordingly
Use when: Triageing vulnerability findings or designing storefront features: deciding where user data is stored (reviews, profiles, messages) versus only reflected in a response (search, filters).
- Classify a potential issue as reflected if the payload must be carried in a link the victim clicks (URL path or query).
- Classify it as stored if the payload is persisted server-side — in a database, cache, or any durable field — and rendered for other visitors.
- Treat stored issues as higher impact because the delivery route is irrelevant: the victim need not click anything from the attacker, so the whole user base is exposed.
- Accept that the entry route for stored payloads can be obscure — an HTTP header, an API import, or a bribed insider — because any route to the data store suffices.
- Prioritise fixes for stored flows: user profiles, uploaded content, review text, and anything that imports external data.
Caveat: This is a classification framework, not a numeric severity scale; actual risk depends on the page and audience.
Caveat: Stored XSS can be reached by means that would be impractical for reflected XSS, so do not use 'the attacker could not get them to click it' as a rejection reason.

Tags: bot-and-agent-security, stored-xss, reflected-xss, input-validation, retention, customer-research
Source: Site Security (1).docx

---

## Escaping cannot defeat breakouts caused by a closing script tag
Use when: Reviewing any storefront or checkout page where user data or third-party content is embedded in a script, or when evaluating page-builder widgets that inject sequences into scripts.
- Understand the parser order: the HTML parser runs first and identifies script boundaries, then a separate JavaScript parser runs on each script body.
- Recognise that including the literal characters for a closing script tag inside a string or comment in JavaScript still terminates the script element and can let an attacker resume HTML context, executing code.
- Do not rely on escape sequences for quotes or backslashes to prevent this, because the boundary is determined before those sequences are interpreted.
- Fix the embedding pattern: hex-encode the data so no breakout characters exist, or keep the data out of script bodies entirely.
- Prefer loading third-party scripts by src from a trusted destination, which avoids this class of problem.
Caveat: The source notes a syntax error in one script generally does not prevent other script elements from running, but the breakout itself is the security concern.
Caveat: This applies wherever user data reaches a script body, including dynamically generated widgets.

Tags: bot-and-agent-security, output-escaping, script-context, pdp, checkout
Source: Site Security (1).docx

---

## Blacklist filtering of tag names fails against forgiving HTML parsers
Use when: Evaluating any input sanitisation that tries to block specific tags or words in customer reviews, product descriptions, or rich-text fields.
- Treat blacklists of tag names (script, style, etc.) as unreliable, because browsers accept unusual whitespace, slashes and other characters between a tag name and its attributes.
- Assume new elements and browser-specific quirks will appear after your blacklist is written.
- Where possible, work from an allowlist of the exact, minimal markup and attributes you intend to support, and escape everything else.
- Understand the robustness principle ('be conservative in what you send, forgiving in what you accept') is why parsers are lenient — that leniency is a security liability for filters.
- Validate changes against real browsers rather than assuming a filter behaves as written, and treat consistency across browsers as unproven.
Caveat: The source notes older browsers differed significantly in how they interpreted unusual characters; modern behaviour is more consistent but still not safe to filter against.
Caveat: This is a validation caution, not a recommendation to write your own full sanitiser.

Tags: bot-and-agent-security, input-validation, allowlist, pdp, customer-research
Source: Site Security (1).docx

---

## Beware DOM-injected globals via user-controlled element IDs
Use when: Designing features that assign element IDs from user input, such as personalised widgets, review anchors, or per-customer page components.
- Recognise that the DOM creates a global JavaScript variable automatically for each element with an ID — this is a DOM behaviour, not a JavaScript feature.
- If a script references a variable that is normally undefined and a user can set an element ID to that name, the condition can flip to truthy and divert the script's logic.
- Do not let users control element IDs or form field names; generate IDs server-side from a safe pattern (e.g. a numeric token) instead.
- Also avoid letting users control form field 'name' attributes, since forms rely on them.
- When reviewing templates, treat any user-controlled identifier as a potential variable-injection point.
Caveat: The source was uncertain how duplicate IDs are resolved, but notes duplicates can change which element JavaScript selects.
Caveat: This is an indirect attack that depends on what your script does with the variable; not every case is exploitable.

Tags: bot-and-agent-security, dom-security, input-validation, pdp, experiment-design
Source: Site Security (1).docx

---

## Use data URLs for small inline assets, not large ones
Use when: Choosing whether to inline small storefront assets such as icons or logos into the page or CSS, versus serving them as separate requests.
- Understand that an inlined data URL travels with the HTML or CSS, so the browser shows the asset on the first response instead of making an extra request, then waiting.
- Inline only genuinely small assets; the source suggests a tiny icon may be worth it while a multi-megabyte image is not.
- Recognise that inlined assets cannot be cached separately, so a large or repeat-viewed asset re-downloads with every page load.
- Use the same technique inside CSS to avoid an extra HTTP request for small background images.
- Weigh the round-trip saved against the added page weight before deciding.
Caveat: The source gives no specific size threshold, only the principle that small is suitable and multi-megabyte is not.
Caveat: Separately, data URLs are a security risk when users can supply them as link or source values — context determines whether they are helpful or dangerous.

Tags: bot-and-agent-security, performance, page-weight, pdp, landing-page
Source: Site Security (1).docx

---

## Fix XSS with Context-Aware Output Encoding
Use when: Reviewing or briefing developers on your storefront's product review fields, search results pages, or any template that echoes customer-supplied content.
- Identify every place customer-controlled data is echoed: product reviews, search query display, cart notes, custom engraving text, account names.
- For each output location, apply the encoding matching that context: HTML-entity encoding in HTML body, attribute encoding inside attributes, JavaScript-string escaping inside script blocks, URL encoding inside hrefs.
- Do not encode only at input or only once: a value written into a JavaScript string and then injected into HTML needs a second round of context-appropriate encoding.
- Avoid deeply nested encoding chains where the same value passes through several languages or contexts; if a value must cross contexts, isolate it into a data attribute or JSON blob rather than embedding it inline.
- Add a review step or linting rule so new template code that echoes user input gets a context check before release.
Caveat: Encode at output, not just input; input filtering alone does not cover stored XSS in reviews or legacy data.
Caveat: The source presenter calls deep nested encoding fragile and advises against it.

Tags: bot-and-agent-security, xss, output-encoding, product-page, input-validation, code-review
Source: Site Security (1).docx

---

## Treat XSS Filtering Browser Features as Unreliable
Use when: Deciding whether browser-level XSS filtering removes the need for server-side sanitization on your storefront's reflected input pages.
- Assume the browser's reflected-XSS filter may decide not to block an attack, or may be absent entirely, and that some bypasses can degrade into new attack classes.
- Keep reflected XSS prevention on the server and in templates: encode output by context and validate input, rather than relying on the browser to strip script from URLs.
- When testing your own storefront, use your own staging copy, not third-party sites.
- Verify the current state of any named browser filter before relying on descriptions of it, since browser behavior and availability change.
Caveat: The source describes this as a historical browser feature; verify its current status before citing it.
Caveat: No filter, header, or browser feature alone guarantees XSS protection.

Tags: bot-and-agent-security, xss, browser-security, output-encoding, verification
Source: Site Security (1).docx

---

## Choose Between Content-Matched and Person-Targeted Ads
Use when: Deciding whether your store should buy content-matched placements (relevant publishers, category pages) or behavioral audiences, and understanding why cheap inventory may outperform contextually relevant inventory on cost.
- For each campaign, state whether the targeting is against content (site, category, article context) or against the person (retargeting pools, lookalikes, cross-site profiles).
- If using person-level targeting, compare effective cost per acquisition on premium publishers versus low-cost long-tail inventory, since the same user may be reachable much more cheaply elsewhere.
- If you are the publisher or content site, recognize that person-level buying reduces the marginal value of quality content and pushes ad revenue toward cheap inventory; budget for this when forecasting content-driven revenue.
- For sensitive product categories (e.g. health, fertility, baby, debt), suppress or exclude person-level audiences where downstream disclosure could harm the customer; the source cites a case where pregnancy-related targeting revealed a pregnancy to a family member.
Caveat: The source's ad-economics discussion is the presenter's analysis, not a measured benchmark for your account.
Caveat: Historical claims about which ad companies were profitable are dated; verify current figures.

Tags: bot-and-agent-security, acquisition, creative-strategy, audience-targeting, privacy, measurement
Source: Site Security (1).docx

---

## Plan for Third-Party Tags as Tracking Surfaces
Use when: Auditing your store's third-party script footprint or preparing a privacy review before adding another analytics, personalization or ad tag.
- Build an inventory of every third-party resource loaded on home, category, product, cart and checkout templates: analytics, pixels, chat, reviews, A/B tools, payment SDKs.
- For each tag, record what data it can observe (URL, referrer, cookies, form contents) and whether it operates in the first-party context.
- Prefer tags that make explicit contractual privacy commitments and avoid others; the source notes some CDNs publish such guarantees, though a published promise is not enforcement.
- On checkout and account pages, minimize third-party scripts because those paths carry payment and identity data.
- Re-audit after each new tool ships, since tags accumulate.
Caveat: The census figures cited are several years old; treat the ~20 third parties and ~70-80% reach as directional, not current measurements.
Caveat: A vendor privacy promise is a legal commitment, not a technical control.

Tags: bot-and-agent-security, third-party-scripts, privacy, audit, checkout, measurement
Source: Site Security (1).docx

---

## Understand Cookies and Third-Party Cookie Exposure
Use when: Reviewing how your store's session, cart persistence and embedded third-party content handle cookies.
- Distinguish first-party cookies (set and read by your own domain) from third-party cookies (set by embedded resources); cart and login typically depend on first-party cookies.
- Audit embedded third-party elements (images, iframes, widgets) and whether they receive cookies on your pages.
- Set session cookies with HttpOnly and Secure attributes where applicable, and scope cookie domains narrowly, so attached third-party resources do not inherit your identifiers.
- Recognize that third-party request cookie behavior has been restricted by several major browsers; verify current behavior in the specific browsers your customers use before assuming a cookie will or will not be sent.
Caveat: Browser cookie policy changes frequently; treat any specific current restriction as subject to change.
Caveat: Secure cookies prevent interception over plaintext, not tracking via other identifiers.

Tags: bot-and-agent-security, cookies, tracking, checkout, session-management, privacy
Source: Site Security (1).docx

---

## Treat HSTS as a Security Feature That Can Be Repurposed
Use when: Reviewing domain and subdomain configuration for your store, especially if you control or delegate many subdomains.
- Deploy HSTS on your storefront domains deliberately, with care about preload and long max-age, since the setting is effectively sticky for returning visitors.
- Inventory subdomains: because HSTS rules can be set per subdomain, a large delegated subdomain space becomes a tracking surface.
- Restrict who can create subdomains and which parties can set headers on them, and retire unused subdomains.
- Treat HSTS as transport protection only; it is not an anti-tracking or XSS control.
Caveat: The subdomain encoding technique is discussed in the source as an observed abuse; do not rely on HSTS to prevent tracking.
Caveat: HSTS configuration mistakes can lock users out of plaintext access; test before preloading.

Tags: bot-and-agent-security, hsts, transport-security, domains, tracking, configuration
Source: Site Security (1).docx

---

## Assess Fingerprinting Risk on Your Storefront Analytics
Use when: Evaluating whether removing third-party cookies actually reduces cross-site tracking of your store's visitors, or choosing an analytics approach for privacy-sensitive audiences.
- List the attributes your site or its tags can read: user-agent string, installed fonts, screen and window dimensions, canvas rendering output, audio rendering output, hardware concurrency, device memory, WebGL parameters, network type.
- Treat any single attribute as non-identifying but the combination as highly identifying, and measure the combined entropy using a tool like the EFF's Panopticlick-style test against your own site.
- If you are the publisher or merchant, note that fingerprinting continues working after cookies are cleared, so cookie-consent banners alone do not stop cross-site identification.
- If you are evaluating privacy tooling, prefer approaches that address the combined fingerprint set rather than any single attribute.
Caveat: Fingerprinting libraries and browser countermeasures change; check current implementations before acting.
Caveat: The source discusses defensive countermeasures and open problems, not guaranteed solutions.

Tags: bot-and-agent-security, fingerprinting, tracking, analytics, privacy, measurement
Source: Site Security (1).docx

---

## Recognize Font Enumeration and Why It Is Hard to Fix
Use when: Evaluating a privacy-preserving analytics or anti-tracking approach that claims to neutralize fingerprinting, to check whether font enumeration is addressed.
- Understand the mechanism: a page iterates a long list of font names, applies each to a test element, and checks if the rendered size changed; changed size implies the font is installed.
- Accept that you cannot block reading element dimensions without breaking page layout, so a simple blocker is not the answer.
- Consider the tradeoffs used in practice: treating local fonts as unavailable is acceptable for many Western sites but breaks some sites, especially in Asian-language contexts where local fonts are commonly required because system fonts are poor.
- Alternative mitigations include mapping a language to a small permitted font set (trading privacy-set size for compatibility) and gating font access behind a permission prompt.
- If you are auditing your own store, note that you almost certainly do not need local font enumeration for legitimate function.
Caveat: The source notes defenses here are unsatisfying and standards work is contested.
Caveat: Permission prompts help only when users decline; network traffic can still reveal font loading.

Tags: bot-and-agent-security, fingerprinting, fonts, privacy, product-page, configuration
Source: Site Security (1).docx

---

## Treat Canvas and Audio Fingerprinting as Unpredictable APIs
Use when: Understanding what browser-based fingerprinting can extract from visitors to your store, or assessing what a privacy tool must suppress.
- Recognize that drawing operations rendered to a canvas can be read back as a blob or data URL and hashed; harmless uses exist (e.g. checking emoji support) but the same API serves fingerprinting.
- Note that audio processing can be fingerprinted either by querying capability information or by generating a waveform and hashing subtle device-specific differences.
- Treat these as hard-to-lie-about signals, since the rendering difference is inherent to the hardware and usually imperceptible to users.
- When evaluating fingerprinting protections, check whether canvas and audio outputs are perturbed or blocked and whether that breaks legitimate functionality.
Caveat: The source describes these techniques as observed in a widely used fingerprinting library; it does not claim they cover every device or browser.
Caveat: Perturbing rendering can break legitimate canvas applications, so blanket blocking is a tradeoff.

Tags: bot-and-agent-security, fingerprinting, canvas, audio, privacy, measurement
Source: Site Security (1).docx

---

## Audit Permissionless Hardware and Network APIs
Use when: Auditing third-party scripts on your store or judging how much identifying data your pages already leak by default.
- Enumerate what scripts on your pages can read without asking: hardware concurrency (CPU cores), Web Audio channel configuration, WebGL shader capabilities, an approximate device memory value, and network-touching APIs that reveal connection type and IP-adjacent details.
- Treat these as available to every script on every page; there is no user-facing consent gate for them in the browsers described.
- When adding a new script or SDK, include these APIs in the review of what that vendor can observe.
- For privacy-sensitive storefronts, consider which scripts genuinely need hardware or network information and remove those that do not.
- Verify the current standardization and browser support for each API before relying on any specific one.
Caveat: Standardization status varies; some APIs are non-standard or Chromium-only per the source.
Caveat: These APIs are not the only identifying sources; they are a subset.

Tags: bot-and-agent-security, fingerprinting, browser-apis, third-party-scripts, privacy, audit
Source: Site Security (1).docx

---

## Treat Viewport Size as the Hardest Fingerprint to Fake
Use when: Assessing how much identifying information your responsive storefront design indirectly exposes, or evaluating anti-fingerprinting tooling.
- Distinguish between querying window dimensions via JavaScript (easy to override) and inferring them by measuring whether an image displays or how text flows (hard to override without breaking rendering).
- Recognize that because the hard method cannot be faked without breaking pages, viewport size tends to be a strong identifying signal.
- When designing responsive storefront layouts, be aware that layout APIs used to measure rendering can serve as fingerprinting side channels.
- If evaluating privacy tooling, check whether it addresses dimension-based identification, not only JavaScript-visible values.
Caveat: Countermeasures here are limited; the source calls it the hardest case.
Caveat: Any specific tool's handling of viewport fingerprinting should be verified for the current version.

Tags: bot-and-agent-security, fingerprinting, viewport, privacy, web-design, measurement
Source: Site Security (1).docx

---

## Use Hashing Aggregation to Reason About Poisoning Fingerprints
Use when: Evaluating anti-fingerprinting approaches or deciding which single signal a protection should target when full masking is impractical.
- Understand the implementation pattern: each input (font set, viewport, canvas output) is separately hashed, then all hashes are combined into one stored value.
- Recognize the implication: altering any one contributing input changes the combined output, so you do not necessarily need to neutralize every signal.
- Treat this as a reason to prioritize which signal is cheapest to randomize reliably without breaking functionality, rather than trying to mask all signals.
- Do not assume this always works: the source notes it is often, not universally, true, and sophisticated implementations may be resilient.
Caveat: The source explicitly qualifies this as 'not always true', so treat it as a heuristic.
Caveat: Randomizing an input may degrade legitimate functionality such as localization or rendering.

Tags: bot-and-agent-security, fingerprinting, hashing, privacy, countermeasures, experiment-design
Source: Site Security (1).docx

---

## Account for Cookie Syncing Across Identifiers
Use when: Understanding why clearing cookies or blocking third-party cookies alone does not sever an existing cross-site profile of your store's visitors.
- Understand the pattern: when a tracker sees a recognized cookie, it stops; when it sees an unrecognized cookie, it fingerprints the browser and links the new cookie to the existing profile.
- Recognize that this makes cookie clearing insufficient on its own to prevent identity linking across sites.
- For analytics and personalization on your store, avoid embedding tracking vendors whose linking behavior you cannot inspect, since identifiers you set may be joined to external profiles.
- Prefer first-party measurement where practical, and document which identifiers (cookies, local storage) your own stack writes so you can reason about linkage risk.
Caveat: The source describes this as an extremely difficult problem to work around; do not present a simple fix as guaranteed.
Caveat: Specific tracker behavior changes; verify current practices of any vendor you use.

Tags: bot-and-agent-security, fingerprinting, cookies, tracking, privacy, measurement
Source: Site Security (1).docx

---

## Check New Tags for Identity-Linking Risk Before Adding
Use when: Before adding a personalization, reviews, chat, A/B testing, or attribution vendor to your storefront.
- Ask what identifiers the tool reads and writes, and whether it operates across other sites where it already has a foothold.
- Check whether the vendor claims to fingerprint or sync cookies with other data; independent value does not require cross-site identity linkage.
- Prefer tools that operate with limited page access and explicit privacy commitments, and confirm whether those commitments are contractual.
- For account and checkout pages, restrict script access to data beyond what the tool needs to function.
- Re-check after vendor updates, since a tool's data collection can change post-integration.
Caveat: Vendor claims and practices change; verify rather than assuming.
Caveat: Independent functionality does not guarantee no cross-site linkage.

Tags: bot-and-agent-security, third-party-scripts, privacy, personalization, audit, checkout
Source: Site Security (1).docx

---

## Set Up a Repeatable External Script Review
Use when: Scheduling a recurring privacy and security review of your ecommerce site, or onboarding a new developer to review standards.
- Establish a checklist that covers every template: home, category, product, search results, cart, checkout, account, order confirmation.
- For each template, record the third-party resources loaded, what data they can read (URL, cookies, form fields, hardware signals), and whether they require permission.
- Note which screens reveal sensitive product interest (health, fertility, baby, financial) where person-level targeting could create downstream disclosure harms.
- Review on a recurring cadence and after each release that adds a tag, script, or integration.
- Spot-check against an available fingerprint-testing tool to see how identifying your own site's configuration makes an average visitor, without assuming any single tool covers all signals.
Caveat: Specific testing tools and their signal coverage change; verify current versions.
Caveat: Automated tests reveal what your own rendering exposes, not what external trackers can infer from elsewhere.

Tags: bot-and-agent-security, audit, third-party-scripts, privacy, process, checkout
Source: Site Security (1).docx

---

## Browser API permission tiers for storefront feature planning
Use when: Deciding when a storefront can trigger clips, sound, fullscreen, vibration, clipboard or camera during PDP video, spin-to-win, or promotional widgets.
- Treat level 0 APIs (DOM manipulation, moving windows, triggering file downloads, hiding the mouse cursor) as callable the moment a visitor lands — no interaction required. Level 0 downloads are the surprising one: a page can deposit a file in a visitor's downloads folder on load, though browsers prompt before a second simultaneous download.
- Treat level 1 APIs (window.open pop-ups, clipboard write, picture-in-picture, vibration) as requiring a user gesture — a click, tap or key press. Scrolling does not count; the call must be made directly inside the event handler for the gesture.
- Treat level 2 APIs (geolocation, camera, microphone, torch/flash) as requiring an explicit permission prompt; a visitor must click Allow before the storefront gets the capability.
- Treat the engagement-gated tier (autoplay with sound) as browser-decided: sites a visitor engages with repeatedly may autoplay audio, others will not.
- Design promotional and video features so their required capability maps to a tier you can realistically reach on first visit, not one that only long-term returning visitors get.
- Verify the current tier assignments in the browsers you support before shipping — several capabilities have moved up a tier over time and the exact list changes.
Caveat: Tier assignments are not contractual and vary by browser and over time; the source's list is a snapshot.
Caveat: Engagement-gated behavior is opaque and unpredictable for developers, so don't build critical functionality on it.

Tags: bot-and-agent-security, product-page, landing-page, browser-apis, conversion-optimization
Source: Site Security (1).docx

---

## UI denial-of-service patterns that can lock down a storefront session
Use when: Auditing suspect third-party scripts, promo takeovers, or scareware landing pages that trap shoppers, and deciding what to add to a monitoring or content-review checklist.
- Understand the mechanism set: intercepting keyboard events so Cmd/Ctrl-W does not close the tab (partly mitigated by triggering an alert/prompt between the Cmd and W keystrokes), pushing extra history entries so the back button cannot escape the page, spawning windows from every captured user event and refocusing them, hiding the cursor via a CSS property, and stacking dialogs on a timer.
- Recognize the commerce-relevant abuse case: scareware pages that claim the device is infected and lock the visitor in to make a purchase pitch more convincing, especially to non-technical shoppers.
- Defend by policy and process rather than by building the same tricks: restrict which third-party scripts run on your checkout and PDP, and screen any purchased traffic destinations for trapping behavior.
- Note the modern mitigation: multi-process browsers can kill a tab stuck in an infinite loop without freezing the whole browser, and file-download prompts limit bulk silent downloads.
- Do not use these techniques on your own storefront — the source frames them as attacks, and trapping visitors is a legal and trust risk, not a conversion tactic.
Caveat: The source describes these as attack patterns demonstrated in a classroom setting; the card converts them into vulnerability recognition and prevention, not reproduction instructions.
Caveat: Some mitigations described are historical and browser-specific; verify current behavior.

Tags: bot-and-agent-security, checkout, third-party-scripts, scareware, abuse-prevention
Source: Site Security (1).docx

---

## GET-request and CSRF exposure in storefront logout and account actions
Use when: Reviewing storefront endpoints for logout, cart mutation, wishlist, subscription pause, and account actions before launch or a security audit.
- Inventory every endpoint that changes server state: log out, add/remove cart line, apply coupon, pause subscription, change email. Flag any that answer to GET.
- Reason about exposure: because any page can cause a GET by embedding an image whose URL points at your endpoint, a visitor to a third-party site can be logged out of your store or have cart state altered without noticing.
- Require POST (with CSRF token) for state-changing operations, and set SameSite on session cookies so a cross-site request cannot carry the shopper's authenticated cookie.
- Check whether your platform already does this and whether legacy endpoints slipped through — the source notes even large providers have left logout-style GET endpoints working.
- When evaluating a third-party integration, ask whether its callbacks to your store use POST with CSRF protection or whether they silently rely on GET.
- Retest after any framework upgrade, since fetch/prefetch behavior and cookie defaults change between versions.
Caveat: The source's Gmail/Google logout example is a case observation, not a claim that any particular store is currently vulnerable; verify your own endpoints.
Caveat: SameSite cookie support and defaults have changed over browser versions; confirm current browser handling.

Tags: bot-and-agent-security, checkout, authentication, csrf, cookies, payment-security
Source: Site Security (1).docx

---

## Client-side fingerprinting surfaces to audit on a storefront
Use when: Reviewing analytics, anti-fraud, or ad-fraud scripts on a PDP or checkout for covert device-based identification, and preparing a data-privacy disclosure.
- Know the surface list: canvas rendering differences, audio via AudioContext capability probing or generated waveform hashing, WebRTC enumeration of device names or IDs (labels or IDs depending on granted permission), installed plugins or unusual Java versions, and font enumeration.
- Expect these to be hard for a shopper to fake — the source notes several are effectively impossible for a normal user to spoof, so relying on them implies persistent identification.
- When evaluating anti-fraud or attribution tools, ask whether they use any of these surfaces and whether that use is disclosed in your privacy notice.
- Watch for the false-security trap: a browser extension that lies inconsistently across surfaces (for example reporting one region on one endpoint and a different preferred language on another) can make a visitor MORE identifiable, not less.
- Plan disclosure and consent around this: aggressive fingerprint-based tracking is a compliance and trust exposure for a store, separate from its effectiveness.
Caveat: The source calls this a representative, not complete, list of fingerprinting methods.
Caveat: Fingerprinting guidance from the lecture includes opinion about tools and is not a legal opinion about what your store must disclose.

Tags: bot-and-agent-security, measurement, privacy, fingerprinting, analytics, anti-fraud
Source: Site Security (1).docx

---

## Choosing a client-side anti-tracking approach for a storefront's third parties
Use when: Choosing how a store handles third-party analytics, tag managers and ad pixels — whether to strip capabilities, standardize, scope by origin, add noise, or adopt a privacy-budget style limiter.
- Option 1 — remove the functionality (disable canvas reads, font enumeration, and similar). Works because benign uses are rarer than abusive ones, but it breaks legitimate use cases and is a losing long-term strategy for a product that wants broad site compatibility.
- Option 2 — standardize the value across browsers so everyone reports the same thing. Conceptually different from removal but functionally close — you have effectively broken the functionality anyway.
- Option 3 — scope access by origin, letting first-party code do more and third-party frames less. The source notes this is a useful primitive but you still need a concrete mechanism to block each specific endpoint, not just a policy about who may use it.
- Option 4 — inject noise via steganography (subtly perturbing high-entropy values so readings are unusable for identification while remaining imperceptible). The speaker rates this as the most promising current approach, with the caveat that a determined fingerprinter can detect and discard the noised values.
- Option 5 — privacy budgets (Google's proposal): enumerate endpoints, assign identifying bits, and stop granting access past a precision threshold. The speaker calls this a bad idea with unresolved scope, lifetime and third-party budget questions.
- Apply to your store by asking which option each vendor actually implements before trusting it; a 'privacy-friendly' label does not tell you which approach is behind it.
Caveat: The ratings (option 4 promising, option 5 bad) are the speaker's opinions, not settled consensus; the privacy-budget proposal is described as an early proposal likely to change.
Caveat: Permission-prompt strategies suffer from well-documented prompt fatigue — visitors reflexively accept, so don't treat prompts as reliable user consent for heavy device access.
Caveat: Engagement-derived permission decisions are hard for developers to reason about and change unpredictably.

Tags: bot-and-agent-security, third-party-scripts, privacy, fingerprinting, consent, consent-fatigue
Source: Site Security (1).docx

---

## Drawing the line between store conveniences and visitor harm
Use when: Deciding whether a growth hack or upsell widget is acceptable — evaluating friction, dark patterns, or aggressive re-engagement tactics at checkout or exit.
- Apply the source's test: is the project making powerful parties more powerful over weaker ones, or making weaker parties stronger against powerful ones?
- Reject the framing that 'privacy is a feature' or a badge on the box; the speaker treats user harm as a failure state, something you owe the visitor, not a differentiator you market.
- Recognize that tactics which make a site intolerable — fake downloads, forced dialogs, breakage on exit — are the same family as attacks, and visitors will leave or disable protection rather than endure them.
- For exit-intent and abandonment flows, prefer a single clear browser-native confirm or a well-designed email capture over stacked or forced dialogs; the source describes stacked dialogs as attack behavior.
- When a legal or technical protection conflicts with a short-term revenue tactic, prefer the protection where the harm is to the visitor, and document the trade-off.
Caveat: The speaker states this as a personal ethical position, not a measured business result.
Caveat: The card applies the principle to ecommerce; the source's examples are attack demonstration sites, not storefronts.

Tags: bot-and-agent-security, retention, conversion-optimization, ethics, dark-patterns, cart-abandonment
Source: Site Security (1).docx

---

## Legal-context limits when relying on existing privacy rules for a store
Use when: Planning store tracking, consent copy, or account features and estimating how much you can rely on law versus technology to protect visitors.
- Treat GDPR as the source's example of the most mature regime, applying to any company selling into Europe regardless of headquarters — a common reason stores adopt EU-grade consent globally.
- Note the US direction of travel (California legislation described as the strongest in the US at the time, weaker than GDPR) and verify current status before making compliance claims.
- Design for a purpose-limitation rule: consent for one use does not authorize another (the source's example — a phone number given for second-factor authentication cannot be reused to link cookies or feed advertising).
- Apply this to store data: if a customer gives an email or phone for order notifications, don't repurpose it for ad targeting or cross-platform identity without separate consent.
- Recognize the enforcement gap: actors outside the jurisdictions you can reach are hard to constrain and hard to measure, so a technical control (blocking, scoping, filtering) must be part of the plan, not only legal language.
Caveat: Legislation described is a snapshot; the California and GDPR descriptions must be re-verified before being written into policy.
Caveat: This is not legal advice — confirm obligations with qualified counsel for your jurisdiction and channels.

Tags: bot-and-agent-security, privacy, compliance, gdpr, customer-accounts, measurement
Source: Site Security (1).docx

---

## Using brand-scoped access decisions rather than trusting page content
Use when: Designing an agent or script that reads storefront pages, vendor documents, or customer messages, or deciding what a first-party integration may do versus an embedded third-party frame.
- Adopt the origin distinction: code served by your own domain is the first party and can be trusted with more of your session; embedded third-party frames are least-trusted and should get the narrowest capability set, enforced by feature-policy-style restrictions.
- Apply the same split to automations and agents: a tool that reads an order confirmation email, a supplier PDF or a product feed is processing untrusted data. Instructions found inside that data are not authorization for the agent to place orders, change prices or move funds.
- Scope each agent or integration to a specific brand, store and task, so a compromised or prompt-injected data source cannot spill into other merchants, catalogs or payment methods.
- Require explicit human approval for state-changing actions (publish price, submit refund, place purchase order) regardless of what the source document says is authorized.
- Encode the rule that a permission prompt, page element, or document claim never overrides your authorization logic — treat them as inputs to be validated, not commands.
Caveat: The source does not use the modern 'prompt injection' vocabulary; the mapping from first/third-party trust to agent data trust is an applied interpretation, not a stated result.
Caveat: Feature policy and frame-level controls vary by browser and are periodically renamed or changed — verify the current mechanism before relying on it.

Tags: bot-and-agent-security, agent-security, authorization, third-party-scripts, permissions, trust-boundaries
Source: Site Security (1).docx

---

## Permission and engagement gating as UX constraints on storefront video and audio
Use when: Planning PDP video, hero autoplay, or promotional overlays that include audio, and deciding whether to mute by default or gate playback behind a click.
- Assume audio cannot autoplay on a visitor's first arrival; browsers gate it behind a user gesture and may relax that based on engagement.
- Capturing the gesture is the realistic path: attach a click listener and call play inside the handler — the call must be made directly in response to the event, not from a deferred callback.
- Expect returning, engaged visitors to behave differently — the source notes sites like YouTube start playing immediately because those users have a history of triggering audio and staying.
- Choose a default: the source notes a well-known demo defaults its video to muted, which sidesteps the gate; a product page promoting a video with sound should either mute by default or use a clear play button.
- Do not build a core purchase path that depends on a capability you may not get on first visit; keep the fallback (poster image, muted loop) as the primary experience.
Caveat: Engagement gating is browser-specific, undocumented at the rule level, and changes over time.
Caveat: The requirement that the call happen inside the gesture handler is a technical constraint that breaks subtle deferred implementations.

Tags: bot-and-agent-security, product-page, landing-page, browser-apis, video, conversion-optimization
Source: Site Security (1).docx

---

## When clipboard and download APIs are acceptable on a storefront
Use when: Implementing coupon copy buttons, share links, invoice or label downloads, or a 'your download is starting' page after purchase.
- Keep clipboard writes tied to a user gesture; a write on any captured interaction can silently replace the visitor's clipboard, and the source describes the abuse of injecting promotional content.
- Never expect clipboard reads without a permission prompt — the source lists this as intentionally gated so a site cannot read what the visitor has copied.
- Use single-programmatic downloads freely: a post-purchase or thank-you page that starts a file download without an extra click is an accepted pattern, and the source identifies that pattern as the reason the capability stays ungated.
- Plan for the multi-download prompt: a second simultaneous file download triggers a browser prompt, so bundle or multi-file downloads need a user click or a zip.
- Consider the version gap: if you want a shopper to trigger actions in a privileged context (local tool, hardware button, permission prompt), note that this space was once Flash territory and verify the modern browser route before building.
Caveat: Browser gating for downloads and clipboard has changed repeatedly; verify current behavior on target browsers.
Caveat: The source's examples are demonstrations, not measurements of storefront conversion effects.

Tags: bot-and-agent-security, checkout, product-page, browser-apis, fulfillment, post-purchase
Source: Site Security (1).docx

---

## Standardizing error and edge behavior to reduce identifying signal
Use when: Diagnosing why anti-fraud or analytics flags certain customer segments, or when configuring a storefront so error responses don't become an identifying signal.
- Understand the mechanism: if a visitor spoofs a user agent, a fingerprinter can break them out by making the browser throw and reading the subtly different error response across browsers and versions.
- Expect the same idea applied to HTML parsing: the source cites a body of work enumerating malformed-HTML cases that both enable code execution and act as fingerprinting surfaces, with standardization of error conditions as the proposed remediation.
- For a store: standardize your own error pages and API error responses so they don't reveal stack details, framework versions or platform identities to scanners and fraudsters.
- Reduce reliance in anti-fraud scoring on browser-version tells that can be spoofed, since a determined actor can and does falsify them.
- Test error behavior across the browsers your shoppers actually use before drawing conclusions from a bot score, since the same visitor may look different from different environments.
Caveat: The source presents this as an area of active research with no complete solution; the error-case work is cited as a paper reference, not a shipped product.
Caveat: Do not treat error standardization as sufficient bot detection or blocking on its own.

Tags: bot-and-agent-security, anti-fraud, measurement, fingerprinting, error-handling, bot-detection
Source: Site Security (1).docx

---

## Budgeting identifying bits across third parties before adding another script
Use when: Prioritizing which analytics, chat, personalization and ad scripts to keep on a checkout or PDP, and evaluating a vendor's 'privacy budget' claim.
- Start from the observation that fingerprinting endpoints vary widely in how much they identify — the source's illustrative attribution is roughly a bit for one endpoint up to about 13 bits for a strong one, and those add up.
- Ask three questions of any budget-style or scoring scheme before trusting it: what happens when the budget is exhausted (do features break?), what is the lifetime of the budget (a fresh allowance per page view makes the scheme meaningless), and does the scope reset per third party?
- Recognize the third-party problem: if each embedded third party gets its own budget, identifiers can be traded across parties; if the budget is shared page-wide, one third party can exhaust the first party's allowance — the source calls both outcomes a game-changer.
- For your store, count the third-party scripts actually running on checkout and PDP and remove any whose marginal value does not justify the added identification.
- Treat privacy-budget proposals as early-stage and likely to change; don't build contractual promises on them.
Caveat: The source states that this proposal likely will not ship in its stated form and calls it a bad idea; that is the speaker's prediction, not a settled outcome.
Caveat: Bit-count attributions in the source are illustrative of the approach, not measured effectiveness for any actual deployment.

Tags: bot-and-agent-security, third-party-scripts, privacy, analytics, checkout, measurement
Source: Site Security (1).docx

---

## Privacy-preserving measurement for store analytics
Use when: Choosing a privacy-preserving analytics approach for store performance reporting, cohorts or vendor-shared benchmarks.
- Understand the model at a high level: it treats a transaction as if it were a survey result and mixes data across a secret-sharing scheme with clustering and timing before reporting, producing privacy guarantees in aggregate.
- Apply it where a store needs aggregate numbers (conversion by cohort, category performance) but does not need per-customer granularity to make the decision.
- Do not expect it to replace operational data you need per-order — privacy-preserving aggregation is for reporting, not fulfillment or customer service.
- Treat specific mechanism details as the source does: presented briefly, complex, and requiring separate study before adoption.
- When a vendor claims differential privacy, ask for the guarantee's parameters and scope, since guarantees are only meaningful with their epsilon-style budget and the population they cover.
Caveat: The source explicitly declines to explain the mechanism in detail and calls it sophisticated and hard to summarize in the time available; don't over-claim what it does.
Caveat: This is a research direction described by a speaker, not a documented storefront result.

Tags: bot-and-agent-security, measurement, privacy, analytics, retention
Source: Site Security (1).docx

---

## Defend storefront links against tab nabbing (reverse tabnabbing)
Use when: Auditing or building outbound links on a storefront, PDP, blog, help center, or email/chat share flow that opens partner, review, ad, or supplier links in a new tab.
- Understand the vulnerability condition: if a link uses target="_blank", the newly opened page receives window.opener pointing back at your store tab and can navigate that tab to an attacker-controlled clone (e.g. a fake login). This is a demonstrated classroom result, not a live incident report.
- As the linking site, add rel="noopener" to every external link that opens a new tab. The source frames this as the standard defense on the linking site.
- In a component-based storefront, add the attribute once in the shared link component so every rendered link inherits it, rather than hunting links manually.
- Confirm your framework versions and current browser behavior before assuming a default; the source notes browser vendors have discussed changing defaults, so verify current behavior rather than assuming target=_blank is safe or unsafe today.
- Do not rely on CAPTCHA, HTTPS, or a WAF for this class of issue; those controls address different problems. HTTPS alone never guarantees the destination is trustworthy.
Caveat: The source presents this as an unsettled area; browser defaults and mitigations (and a proposed isolation header) may change, so verify against current browser documentation.
Caveat: This card is about links your store produces outward, not about fixing a third party's site.

Tags: bot-and-agent-security, storefront-security, browser-security, link-integrity, third-party-integrations, csrf
Source: Site Security (1).docx

---

## Use SameSite cookies to block cross-site state-changing requests
Use when: Configuring session cookies for customer login, cart, or admin accounts, or reviewing whether an authenticated action (e.g. cart change, address update, admin mutation) can be triggered from a third-party page.
- Recognize the CSRF conflict: an attacker page can point an image, form action, or similar request at your store and the browser may attach the victim's cookies to it. The source notes some large providers have historically appeared vulnerable to this pattern.
- State-changing operations should use POST (or equivalent), not GET-through-an-<img>; a GET URL that logs a user out or mutates state is inherently abusable.
- Set SameSite on session/auth cookies. Strict sends cookies only on top-level navigations from your own site and withholds them on cross-site requests; Lax sends them for normal navigations but blocks them from cross-site subrequests. Treat Lax/Strict as the source's two documented modes and choose per flow.
- Test the tradeoff: Strict can break legitimate cross-site return flows (e.g. returning from a payment or identity provider). Lax is the source's practical compromise for flows that need a normal navigation with cookies.
- Independently verify your CSRF token strategy; SameSite reduces but does not by itself guarantee protection for every browser or legacy flow.
Caveat: The source explicitly says it is uncertain why some major sites appeared to remain vulnerable, so do not treat SameSite as a proven universal fix.
Caveat: Strict can break payment/SSO return journeys; validate your checkout flow before switching.

Tags: bot-and-agent-security, csrf, checkout-security, customer-accounts, session-management, cookies
Source: Site Security (1).docx

---

## Recognize IDN homograph attacks against lookalike domains
Use when: Training support teams, reviewing brand-domain monitoring, or designing login and admin flows where a customer or staff member might be steered to a lookalike domain via a link in a chat, ad, or email.
- Vulnerability condition: a hostname can be built from non-ASCII Unicode letters (e.g. Cyrillic) that are visually identical to Latin letters, so the rendered URL looks like the real brand while the bytes differ. This is a demonstrated condition, not a claim about your store.
- Know browser rendering heuristics: browsers may show a domain in 'punycode' (the xn-- form) instead of the Unicode characters when the domain mixes scripts or contains look-alike characters against a non-international TLD. The exact rule differs by browser and version, so verify current behavior rather than trusting a screenshot.
- Note the known weakness: if the whole domain is composed of one non-Latin script, browsers have historically displayed it as normal text and the look-alike can pass unchecked. The source says some browsers still had not fixed this at the time of the recording.
- Practical controls: use a password manager for staff/admin accounts so credentials are never auto-filled on an unrecognized origin; use hardware security keys where possible; keep an eye on brand lookalike registrations.
- Communicate simply: teach staff to read the registrable domain (the part just before the first single slash, roughly the last two dot-separated labels), not the full URL from the left, because attacker-controlled subdomains are prepended.
Caveat: Browser URL rendering changes over time; the 2017-era examples may not match current interfaces.
Caveat: The source notes HTTPS padlock and extended-validation UI do not reliably signal trust and historically did not prevent this attack.

Tags: bot-and-agent-security, phishing, domain-security, customer-accounts, brand-protection, password-managers
Source: Site Security (1).docx

---

## Be skeptical of HTTPS padlock and EV badges as trust signals
Use when: Deciding which trust indicators to display on a storefront or checkout, or explaining to customers and staff why a padlock is not a legitimacy guarantee.
- Understand the distinction: a secure connection means you are talking to the server named in the certificate over encryption. It does not establish that the operator is who they claim.
- Recognize the incentive: certificate authorities are automated and commercial, and free issuance (e.g. the source's mention of Let's Encrypt era behavior) means anyone controlling a domain can obtain a certificate with no human review. Treat certificate issuance as evidence of domain control only.
- For storefront design: do not present a padlock or 'secure' badge as proof of legitimacy in your own UI; that reflects your site, and the customer's browser UI is a separate, attacker-spoofable surface.
- Keep real controls on the sensitive paths instead: password managers, hardware security keys, and verifying the registrable domain.
- Do not claim HTTPS, hashing, CAPTCHA, a WAF, or prompt filtering alone guarantees security in policy or marketing copy.
Caveat: Certificate issuance policies and browser UI (e.g. EV treatment) change; verify current practice before citing specifics.
Caveat: This covers why padlocks are insufficient, not how to configure TLS.

Tags: bot-and-agent-security, tls, phishing, trust-signals, storefront-security, checkout-security
Source: Site Security (1).docx

---

## Defend against clickjacking that overlays fake trusted UI
Use when: Reviewing whether your checkout, login, admin, or consent pages can be embedded by third parties, and hardening framing headers for sensitive store surfaces.
- Vulnerability condition: an attacker page embeds or overlays your interface under a decoy visual so the user clicks the real hidden control (the source calls this clickjacking and notes cookie-drag variants). The demonstration is a classroom result; treat it as a vulnerability pattern.
- As the framed site, send an anti-framing header (the source references X-Frame-Options) on sensitive pages so browsers refuse to render them in third-party frames.
- Understand the relevant cookie-mode distinction the source notes: with Strict SameSite, a cross-site request that relies on navigation may not carry cookies, which reduces some overlay utility, but this is a partial layer, not a complete frame defense.
- Test in an owned staging environment whether your checkout, login, and admin pages can be embedded from a different origin you control; document the result rather than assuming.
- Combine with password managers and hardware keys for authentication so a mis-clicked overlay cannot yield reusable credentials.
Caveat: The source's demonstrations are historical and some attacks were later blocked by browser changes; verify current browser support for framing headers.
Caveat: Frame headers alone do not stop all overlay tricks on other surfaces.

Tags: bot-and-agent-security, clickjacking, storefront-security, checkout-security, frame-options, browser-security
Source: Site Security (1).docx

---

## Manipulated browser history and UI-suppression tricks are perception attacks
Use when: Assessing how a visitor could be convinced a phishing page is a trusted store (e.g. a fake bank or brand login reached from an ad, chat link, or QR code) and choosing defenses that do not rely on browser chrome.
- Vulnerability condition: a page can cause top-level navigations that appear in the visitor's history (the source describes opening a popup to a search and navigating a window it holds a reference to). Frames do not add history entries because they are not top-level navigations.
- Recognize the UI-hiding variant: the source shows a page embedding an inner scroll region so the browser hides and never restores its own chrome, letting the page draw a fake URL bar. This is a demonstrated technique, not a claim about current browsers.
- Treat all of this as an attack on human perception, per the source: there is often nothing wrong with the code being attacked, only with the UI cues people rely on.
- Better defenses: password managers (which bind credentials to a known origin and will not autofill on an unfamiliar one) and hardware security keys (which will not release the secret to the wrong site).
- Assume a segment of users will end up on a sketchy page and layer in reputation warnings (safe-browsing-style) rather than expecting users to read the URL bar accurately.
Caveat: These specific demonstrations are historical and reported as fixed or dependent on access to another site's window reference; verify current browser behavior.
Caveat: The source explicitly says there is no easy way to defend a site against a picture-in-picture fake-browser attack.

Tags: bot-and-agent-security, phishing, browser-security, customer-accounts, password-managers, hardware-keys
Source: Site Security (1).docx

---

## Verify what your URL bar actually shows before trusting subdomains
Use when: Writing security education for staff or customers, and evaluating whether a URL in a support ticket, ad, or partner link is a real brand domain versus a lookalike subdomain.
- Vulnerability condition: subdomains are free to create, so an attacker can register any domain they control and prefix it with a brand name (e.g. brand.com.webapps.example-attacker.com). The registrable domain is the part before the first single slash, roughly the last two dot-separated labels.
- Know that browsers differ: the source observed Chrome and Safari rendering the whole hostname in black and greying only the path, while Firefox greyed out the subdomain to highlight the registrable domain. Verify the current behavior in your target browsers.
- Test the shrinking case: when the window narrows, browsers may show only part of the hostname, and the source shows a lookalike subdomain can appear safe ('looks like PayPal'). Do not trust a truncated URL bar.
- Operationalize for ecommerce: in support and staff training, tell people to locate the first single slash and read left to the registrable domain rather than reading the URL left to right.
- Additionally, monitor for and file takedowns of brand-prefixed lookalike subdomains and typo-squatted domains, and use password managers/hardware keys on seller and admin logins.
Caveat: URL bar rendering is browser-specific and changes over time; treat the described behaviors as observations at the time of recording.
Caveat: The registrar/domain-attribution rule is a heuristic for reading URLs, not a security control.

Tags: bot-and-agent-security, phishing, domain-security, brand-protection, customer-accounts, staff-training
Source: Site Security (1).docx

---

## Treat browser UI/API features as a security-vs-capability tradeoff with fingerprinting cost
Use when: Deciding whether to add a browser-capability-dependent storefront or checkout feature (device APIs, media capture, sandbox/iframe isolation requirements) and judging the customer-risk tradeoff.
- Apply the source's rough usefulness metric: if a feature were disabled, how many real sites break? Widely used capabilities (e.g. video/voice calling in the source's example) carry high benefit; rarely used ones (the source's example: vibration) are harder to justify.
- Apply the rough cost metric: how much code does the feature add and how often has it been implicated in browser vulnerabilities? More code and more exploit history mean higher risk.
- For an ecommerce feature decision, ask whether the capability is on a customer-trust-critical path (checkout, login, payment, account) or a low-stakes path; be more conservative on trust-critical paths.
- Prefer build defaults that do the right thing rather than a prompt for every capability. The source cites research that users click through prompts heavily (fewer than a quarter of Chrome malware/phishing warnings and a third of Firefox SSL warnings were clicked through, versus about 70% on older, poorly designed Chrome SSL warnings), so prompt design and frequency matter.
- Do not rely on security prompts as your only control; combine defaults with isolation and authentication controls. Note the source's counterintuitive finding that early-adopter/beta users clicked through phishing warnings at higher rates than average.
Caveat: The usefulness metric is explicitly described as rough; it is a judgment aid, not a benchmark you can cite as fact.
Caveat: The prompt click-through figures are from a 2010-era research context and should be treated as historical, not current browser behavior.

Tags: bot-and-agent-security, browser-security, fingerprinting, product-decisions, experiment-design, measurement
Source: Site Security (1).docx

---

## Check URLs against a safe-browsing list without leaking full browsing history
Use when: Evaluating or implementing URL reputation/abuse-warning tooling for a storefront, link shortener, or marketplace, and deciding between real-time URL submission and a downloaded prefix list.
- Recognize the naive approach and its two costs: sending each URL in the clear to the reputation service leaks the full request (and by extension browsing behavior) and adds latency because the check must complete before loading.
- Alternative: download a large list of suspicious URLs locally to avoid latency, but accept that the list is constantly changing and enormous. The source frames both as workable but inferior.
- A better model: the provider hashes suspicious URLs, keeps a list of hash prefixes, and distributes only the prefixes to clients. The client hashes each URL it inspects the same way, takes the prefix, and checks membership locally.
- Consequence of prefix matching: a match means the URL may be unsafe, not that it definitely is; treat a hit as a candidate for a fuller check rather than a verdict.
- Apply the principle to ecommerce tooling: prefer local/prefix-based reputation checks over submitting every customer or staff destination URL to a third party, and log which tool used which data source.
Caveat: The source describes the protocol at a high level and defers detailed mechanics to a later session; verify current provider documentation before implementing.
Caveat: Hashing obscures the URL but prefix lists are an approximation and produce false positives.

Tags: bot-and-agent-security, safe-browsing, reputation, privacy, integrations, measurement
Source: Site Security (1).docx

---

## Design browser security around an assumed-sketchy-site layer
Use when: Deciding how much friction to add to storefront security prompts (login, payment, download, permission requests) and where to invest instead.
- Adopt the source's framing: UI security is an attack on human perception, so plan for the case where the visitor is on a sketchy page rather than trying to prevent every such visit through warnings.
- Keep tasteful, well-worded prompts in specific high-value places where research shows they work, per the source's reading of the prompt-effectiveness paper; avoid showing prompts constantly.
- Add an independent protective layer (browser/store warnings, password managers, hardware keys) that works even when the page's own UI is misleading.
- For your own store, keep prompts on sensitive flows specific and actionable, and test whether a prompt is understood rather than assuming more warnings equals more safety.
- Recognize the underlying tension the source describes between the browser as a simple document viewer and as a powerful app platform; this tradeoff does not go away and should be acknowledged rather than claimed solved.
Caveat: Presented as an ongoing design tension with no settled solution; do not present prompt counts or warning text as a guaranteed control.
Caveat: Click-through statistics cited are historical research figures, not current benchmarks.

Tags: bot-and-agent-security, phishing, prompt-design, customer-accounts, conversion-optimization, browser-security
Source: Site Security (1).docx

---

## Scope untrusted content and tool output as data, not authority
Use when: Designing or reviewing ecommerce automation (order bots, support agents, listing tools, integrations) that reads external content or tool output and can take store actions.
- Treat any retrieved document, web page, email, review, or tool response as untrusted data. Do not let it authorize actions such as refunds, price changes, credential changes, or fulfillment edits.
- Bind permissions to the brand and the task: an agent that manages listings should not hold payment or customer-account credentials, even if a retrieved document asks it to act.
- Require explicit human approval for irreversible or financially material actions, and log which actor, tool, and source triggered each action.
- Keep secrets out of retrieved content and tool output where possible; store credentials in a scoped secret store and reference them by role rather than pasting them into prompts or configs.
- Rely on authentication/authorization, encryption, hashing, and signing as distinct controls: authentication proves the caller, authorization scopes what they may do, and no reputation list or prompt filter substitutes for either.
Caveat: No single control (HTTPS, hashing, CAPTCHA, WAF, prompt filtering) guarantees security; layer controls and verify against current platform documentation.
Caveat: This card transfers the source's phishing/untrusted-content principle to agent tooling; the source itself did not test agent permission models.

Tags: bot-and-agent-security, agent-security, authorization, secrets-management, logging, integrations
Source: Site Security (1).docx

---

## Convert an embarrassing-history or fake-UI trick into a customer-protection test
Use when: Running a defensive review of storefront pages, popups, and iframes that could be repurposed by an attacker, or training support staff to recognize manipulated browser UI.
- Frame each technique as a condition to check on owned systems: can a third-party page cause a top-level navigation from my store, can my checkout be framed, can an overlay hide my own controls, and does my session cookie ride along on cross-site requests.
- Test only in owned staging environments and with accounts you control; do not attempt these techniques against third-party sites.
- Record findings as concrete controls to add (rel=noopener on outbound links, anti-framing headers on sensitive pages, SameSite cookie mode, POST for state changes) rather than as payloads.
- For each control added, note the residual risk: frame headers do not stop every overlay, and SameSite strict can break legitimate cross-site returns such as payment provider redirects.
- Re-verify after browser or framework upgrades, since the source's own examples were fixed by vendors over time.
Caveat: Omit or avoid reproducing payload recipes; this card deliberately describes conditions and defenses only.
Caveat: The source's demonstrations are classroom and historical; do not present them as current live exploitable behavior without verification.

Tags: bot-and-agent-security, security-testing, storefront-security, checkout-security, browser-security, policies
Source: Site Security (1).docx

---

## Use Safe Browsing hash-prefix lookups to block malware/phishing destinations
Use when: Deciding how to screen outbound links, user-submitted content or redirect URLs (e.g. affiliate links, UGC product listings) against known malicious destinations without leaking every URL to a reputation service.
- Understand the mechanism: a reputation service hashes reported malicious URLs (e.g. SHA-256), keeps the full hashes, and distributes only truncated hash prefixes to clients so the download stays small.
- On the client, hash a candidate URL the same way and compare its prefix to the downloaded list. If the prefix is absent, the URL is guaranteed not to be in the known-malicious set (a clean pass).
- If the prefix matches, treat it as 'maybe malicious' only, because chopping the hash introduces collisions. Send the prefix (not the full URL) to the service to fetch the full hashes sharing that prefix, then confirm an exact match.
- Account for evasion: attackers can randomize query strings, so the lookup should test multiple URL variants — e.g. the full path, progressively trimmed paths, and the site home page — rather than one exact URL. A hit on the home page blocks the whole site.
- As an ecommerce operator, apply this to any place you accept or forward third-party URLs (user reviews, affiliate feeds, image/link uploads) and to protecting your own checkout redirect chain.
- Treat the list as one layer of defense-in-depth; it will always miss fresh or never-reported URLs.
- Note the privacy trade-off: even prefix-only queries leak that a user visited some URL sharing that prefix, and repeated queries from one IP can be correlated over time.
Caveat: Hash-prefix checking is a blacklist approach and is guaranteed to miss unseen or newly created malicious URLs.
Caveat: Truncated-prefix collisions mean a prefix hit is not proof of malice — always confirm with the full hash.
Caveat: A whitelist-only approach is impractical for dynamic URLs (query strings, unique document keys) since it blocks anything the service has not seen.
Caveat: If you implement this yourself, verify the current Safe Browsing API behavior and rate/format requirements before relying on it.

Tags: bot-and-agent-security, url-reputation, malicious-links, blacklisting, defense-in-depth, safe-browsing, integrations
Source: Site Security (1).docx

---

## Why hashing is used for integrity and lookup, and what its properties guarantee
Use when: Choosing or reviewing a hashing scheme for things like URL/entity reputation lists, file-integrity checks on uploaded assets, or tokenizing customer data for lookups.
- Pick a hash function that is one-way: given the output you cannot feasibly recover the input, so a leaked hash list does not directly expose the original URLs or IDs.
- Confirm determinism: hashing the same value twice yields the same output, which is what makes prefix/equality lookups possible across many clients.
- Confirm speed: the function must be fast enough to run on every candidate URL or request, since lookups happen frequently.
- Confirm collision resistance: it should be infeasible to craft an input that produces a chosen hash value — important if a passing hash is treated as authorization for a safe/valid object.
- Confirm avalanche behavior: a tiny change to the input (e.g. one query parameter) should drastically change the output, which is what stops trivial near-duplicate evasion of a hash-based blocklist.
- Distinguish this from encryption and signing: hashing is for compact comparison and integrity, not for confidentiality of recoverable data or for proving authenticity by itself.
Caveat: Truncating a hash (as with hash prefixes) deliberately weakens it — collisions become expected, so a truncated match is a candidate, not a verdict.
Caveat: Hashing does not make an input safe or authenticated; it only lets you compare values without storing the raw values.

Tags: bot-and-agent-security, hashing, integrity, lookups, encryption-vs-hashing, data-protection
Source: Site Security (1).docx

---

## Model side channels on your storefront: a correct system can still leak data
Use when: Threat-modeling your storefront or admin pages for what a third-party script or an embedded attacker page could infer about logged-in customers, cart state or history.
- Recognize the definition: a side channel is leakage from a correctly implemented system, via timing, layout, power, size or sensor readings, not from a logic bug.
- Inventory the observable differences your pages create for logged-in vs logged-out users: response sizes, layout width shifts, redirect targets, timing of protected vs public responses.
- Assume any state that changes rendered output (button labels, banner widths, item counts) can be measured by a third-party page that embeds a request to your origin.
- Reduce precision and observability: make protected and public code paths take similar time, keep response sizes consistent, and avoid conditionally rendering elements whose dimensions reveal account state.
- Treat repeated embedding of your URLs in untrusted pages as a fingerprinting channel; limit what cross-origin embeds can trigger on your domain.
- Operate under the source's framing: side channels are everywhere and very hard to fully prevent, so prioritize the ones that reveal account status, payment state or order contents.
Caveat: Most demonstrated attacks (reading QR codes via ambient-light sensor, recovering speech via gyroscope) are proof-of-concept and may be impractical in real conditions.
Caveat: Fully eliminating side channels is not achievable; mitigations reduce precision or rate rather than guaranteeing elimination.

Tags: bot-and-agent-security, side-channel, timing-attack, fingerprinting, threat-modeling, privacy
Source: Site Security (1).docx

---

## Fix visited-link and history leaks: browser whitelists, timing and lying APIs
Use when: Handling links to third-party or user-submitted destinations on product pages and deciding which link styling is safe to let influence layout or resource loading.
- Understand the leak: browsers render :visited links differently, and a page can read style or trigger resource loads to learn whether a visitor has been to a URL, exposing browsing history at scale.
- Whitelist CSS properties for visited links so styling cannot cause layout, size or resource-loading side effects — restrict visited styling to color, underline, weight and similar non-layout properties.
- Make the browser's internal handling of visited vs unvisited links take equal time, so timing the href change or redraw does not reveal state.
- Have the browser report unvisited styles when script queries computed styles of visited links, so direct inspection lies rather than leaks.
- Accept that the fix is incomplete: rendering-time differences (e.g. expensive text-shadow on visited links) can still be measured with requestAnimationFrame timing, especially with many links and large shadow radii.
- For your own store, avoid relying on :visited for anything functional and be cautious about heavyweight visual effects on link-heavy pages if you handle untrusted links.
Caveat: The source presents the 2010 browser mitigation as partial — later timing-based demonstrations still recovered visited history.
Caveat: Some listed attacks require specific browser implementation details that may have changed; verify current behavior rather than assuming it still holds.

Tags: bot-and-agent-security, visited-links, history-leak, css, timing-attack, privacy
Source: Site Security (1).docx

---

## Prevent cross-origin state leaks via embedded images and layouts
Use when: Designing or reviewing any partner widgets, tracking pixels or third-party scripts that embed requests to your logged-in domains on a storefront or admin panel.
- Recognize the mechanism: when a page requests an image from another origin, the browser automatically attaches that origin's cookies, so the returned asset can be conditioned on the victim's login state.
- Understand the leak channel: if a logged-in response (e.g. a 'Log out' button) differs in width from the logged-out response, an attacker page can detect the layout shift and infer account state.
- Apply the fix: use SameSite cookies so that cross-site requests do not carry session cookies, causing the embedded resource to always render as logged-out.
- Audit any images, pixels or embeds that hit your authenticated origins and can be included from arbitrary third-party pages.
- Treat distinguishing logged-in vs logged-out as valuable to phishers, since it lets them pick which brand to impersonate.
- Combine with consistent asset sizing so conditional states do not also leak via width or height differences.
Caveat: This is described as an inherent leak from how same-origin policy interacts with image embedding rather than a single implementation bug.
Caveat: SameSite is the principal mitigation; without it, correctly implemented pages still leak login state.

Tags: bot-and-agent-security, same-site-cookies, image-embedding, login-state, phishing, cross-origin
Source: Site Security (1).docx

---

## Decide how to handle ambient-light and sensor APIs on your storefront
Use when: Deciding whether to use device-sensor APIs (light, motion, orientation) in responsive storefront features and how to bound the risk of the data they expose.
- Recognize the risk pattern: if a page can show or hide white/black or colored content and then read an ambient-light sensor, it can confirm which of two visual states it caused, leaking visited-link status, browser state or image contents.
- Note that the same pattern was shown to extract a QR code: zoom into one square, read the light value to determine black vs white, and iterate to reconstruct sensitive content.
- Treat motion/gyroscope access as a similar channel — high-precision readings can capture acoustic vibration, effectively bypassing microphone permission if exposed without restriction.
- Mitigations browsers considered or shipped include putting the sensor behind a permission, limiting the frequency of sensor readings, and quantizing (reducing) the precision of sensor output.
- For your own store, prefer explicit user-granted permissions rather than silent sensor access, and do not build features that depend on reading sensor data while showing attacker-controllable content.
- Verify current browser vendor and OS behavior before relying on any sensor API — availability and permission requirements have changed over time.
Caveat: The source notes these attacks are often impractical (full-screen, slow, visible) but were serious enough to make browsers reconsider shipping sensor APIs.
Caveat: Sensor permission and precision behavior is browser- and OS-version-specific and changes; do not assume a current configuration.

Tags: bot-and-agent-security, sensor-apis, ambient-light, gyroscope, privacy, permissions
Source: Site Security (1).docx

---

## Prevent command injection in server-side features like file or report generators
Use when: Building or reviewing any server-side feature that shells out — file viewers, image converters, PDF/CSV exporters, backup scripts — triggered by storefront or admin input.
- Identify the vulnerability: concatenating untrusted input (URL params, form fields, cookies, headers) into a string passed to a shell interpreter lets attackers append commands using shell syntax like semicolons.
- Verify the impact: injected input can execute arbitrary OS commands on the server — listing directories, reading files, creating or deleting files, or worse.
- Fix the root cause: do not build a command string from program name plus user data. Use an API that takes the program and an argument array (in Node, spawnSync with ['cat', ...args] instead of execSync with a concatenated string) and escapes arguments for you.
- Run the child process with least privilege and validate/allowlist expected arguments (e.g. permitted filenames or extensions) rather than trusting the raw value.
- Keep the server bound to a restricted interface during development/testing so you do not expose a vulnerable demo to the network.
- Understand that error handling and output should not echo raw command output back to the client if it can reveal filesystem contents.
Caveat: The escaping function differs by language and framework; verify the safe API for your stack rather than assuming one exists.
Caveat: Escaping arguments protects against shell metacharacter injection but does not make an arbitrary file viewer safe by itself — still restrict which files or operations are allowed.

Tags: bot-and-agent-security, command-injection, input-validation, server-security, child-process, least-privilege
Source: Site Security (1).docx

---

## Recognize code injection as the parent category behind XSS and similar bugs
Use when: Reviewing how any user-supplied value reaches an interpreter (HTML, SQL, shell, template) on your storefront, checkout or admin tooling.
- Define the pattern: code injection occurs when the interpreter processes a mixture of programmer-written code and untrusted user-supplied data.
- Understand the failure mode: the interpreter cannot distinguish user data from programmer commands, so attacker input is executed as instructions.
- Note the escape technique: attackers break out of the data context using a special character (a quote, semicolon, or similar syntax) and start writing code.
- Treat XSS as one concrete instance of this broader category, alongside command injection, SQL injection and template injection.
- Apply the general fix principle: keep code and untrusted data strictly separate, and escape or parameterize user data before it reaches any interpreter.
- Recognize that the client controls everything it sends — URL, body, cookies, headers — so all client-provided input must be treated as untrusted.
Caveat: The correct escaping/parameterization mechanism is interpreter-specific; a fix for one context (e.g. HTML) does not protect another (e.g. SQL or shell).

Tags: bot-and-agent-security, code-injection, input-validation, xss, sql-injection, server-security
Source: Site Security (1).docx

---

## Prevent command injection with argument arrays, not string templates
Use when: You are building storefront features that shell out to a tool — image resizing, PDF generation, label printing, inventory export scripts, or any admin automation that runs a program on user-supplied values.
- Identify every place in the store backend where a user-controlled value (filename, SKU, uploaded asset name, search term) is concatenated into a command string.
- Replace string concatenation with the API that takes the program name plus an array of arguments; in Node-style runtimes the source used spawnSync with an argument array, and equivalent functions exist in Python, Ruby and other languages — verify the current API for your runtime version.
- Rely on the runtime to escape each argument so quotes, semicolons and other attacker-controlled characters are treated as literal data, not shell syntax.
- Confirm the semantics: the call should run exactly the named program with those arguments and nothing else, and should reject attempts to append a second command.
- Check the return shape — the source found the API returns a child-process object rather than stdout, so inspect the exit status and read the captured stdout on success and stderr on failure, and surface the failure to the operator instead of silently continuing.
- Treat escaping as only one control: if the command itself is dangerous because the user can choose any file, path or target, fix that separately with an allowlist of permitted files/directories and an authorization check on the requesting account.
- Validate on your own staging environment with benign but tricky inputs such as a filename containing a semicolon and a filename containing quote characters, and confirm no second process runs.
- For admin or agent automation, require that the tool allowlist is defined by the brand, log every invocation with the requesting user, and treat any retrieved text or document as data that cannot expand the allowed command set.
Caveat: Escaping alone does not make an inherently dangerous command safe — the source explicitly notes that if the produced command is one you don't want to run, nothing protects you.
Caveat: The source presentation is a classroom demonstration on a deliberately vulnerable app; do not test injection strings against third-party or production systems you do not own.
Caveat: Argument-array APIs and their exact behavior differ across languages and versions; verify the current interface rather than assuming.
Caveat: Do not claim that using argument arrays guarantees security — it removes one class of injection but not path traversal, authorization gaps or bad command design.

Tags: bot-and-agent-security, code-injection, input-validation, admin-automation, agent-tools, least-privilege, logging
Source: Site Security (1).docx

---

## Recognize and close SQL injection in store login and lookup queries
Use when: You are reviewing or building store account login, order lookup, coupon validation, search filters, inventory reports or any admin query that embeds form input or URL parameters into SQL.
- Map every query that mixes a literal template with request values — login forms and any 'find by email/SKU/coupon' route are the highest-value targets.
- Understand the failure modes you are defending against: an attacker who can change the query can read any table, modify rows, run administrative operations such as dropping tables, and in some database configurations execute operating-system commands, which is effectively full server takeover.
- Replace string interpolation with parameterized queries or prepared statements that bind values separately from the query structure, so user input can never alter the query's shape.
- Where the schema permits it, tighten the query's intent: the source's login example uses a get-style call intended to return at most one user row, which also rejects multiple statements in that API — but the source warns that other APIs in the same library (an exec-style call that supports multiple statements) do not give you that protection, so never rely on it.
- Do not store or compare plaintext passwords; the classroom example kept them in plain text for demonstration only. Hash with a current password-hashing algorithm and verify credentials through the hash, and verify current recommended parameters for your platform.
- Restrict database credentials so the application account cannot drop tables or run administrative statements, and separate read paths from write paths.
- Log failed login and lookup attempts for anomaly detection, but write the log with a parameterized insert — the source shows a logging insert as an attack vector when it is built from string concatenation.
- Validate on your own environment: submit a benign value containing a single quote to the login and search fields and confirm it is treated as ordinary text with no error page or behavioral change.
Caveat: Single-quote testing is a diagnostic signal, not a proof of absence — a quote causing a different response suggests vulnerability, but a normal response does not by itself prove safety.
Caveat: The source's examples are classroom demonstrations on an intentionally vulnerable bank app; do not run these strings against systems you do not own, and do not include working payload recipes in team documentation.
Caveat: WAFs, input sanitizers or ORM usage do not by themselves guarantee safety; parameterization plus least-privilege database accounts is the durable control.
Caveat: Verify current database driver and ORM behavior rather than assuming a specific API's protections.

Tags: bot-and-agent-security, sql-injection, input-validation, authentication, customer-accounts, least-privilege, logging
Source: Site Security (1).docx

---

## Understand and bound blind SQL injection as an operational risk
Use when: You are assessing the risk profile of a store search, filter, order-status lookup or API endpoint that returns a generic success/failure response, and deciding how much effort detection and parameterization deserve.
- Accept that absence of echoed query results does not mean an injection point is low risk; the source describes two blind variants.
- Variant one, boolean/error-based: the attacker constructs a condition and learns the answer because the page responds differently — for example a matched row returns an array where the code expected a single value and the handler crashes — so an observable difference between error and non-error states becomes a yes/no oracle.
- Variant two, time-based: the attacker embeds an expression that deliberately runs slowly (the source's example builds a large blob, converts it to a hex string and uppercases it, costing roughly a third of a second) inside a conditional, so a slow response means true and an immediate response means false, and measurement of response time answers the question.
- Recognize that the attacker can iterate character by character — the source's script tested each letter of a password by checking a substring condition and assembled the whole password regardless of password complexity, because only a timing difference was needed per character.
- Defend by parameterizing queries so the injected condition never executes, by adding rate limiting and anomaly alerts on repeated near-identical requests or unusual response-time variance, and by keeping error pages generic so error/non-error is not a clean oracle.
- Validate only on your own systems using timing measurement and error-message inspection to confirm parameterized queries produce uniform behavior; do not attempt randomized extraction against third parties.
- Note that timing-based defenses are probabilistic — network jitter and load affect measurement, so treat timing anomalies as a signal for investigation, not as proof.
Caveat: The timing values in the source are demonstration artifacts of a specific query on a specific machine, not a benchmark for detection thresholds.
Caveat: Blind extraction is described as requiring creativity and patience; the source notes it is harder than visible-output injection, so prioritization should still weight visible-output endpoints higher.
Caveat: Do not present error-page suppression or a WAF as a guarantee — both reduce signal for attackers but do not fix the underlying injection.
Caveat: Time-based detection is noisy in real traffic; confirm before acting on alerts.

Tags: bot-and-agent-security, sql-injection, measurement, api-security, monitoring, input-validation
Source: Site Security (1).docx

---

## Layer safe-browsing-style URL reputation using local hash prefixes
Use when: You are evaluating or implementing a link-safety or phishing-warning feature for a storefront — for example scanning user-submitted review links, affiliate URLs, supplier links or outbound links in marketing content before they are shown or clicked.
- Understand the naive design and its two costs: querying a reputation service in real time for every URL sends your full browsing or link data to a third party and adds latency because nothing loads until the answer returns.
- Downloading the entire malicious-URL list locally removes the latency and privacy problem but the list is constantly changing and very large, so a full download is impractical for repeated refresh.
- Adopt the prefix approach: the provider hashes each known-malicious URL, truncates each hash to a prefix, and distributes only the prefix set, which the client caches locally.
- To check a URL, hash it with the same algorithm (the source describes SHA-256) using the same transformations the provider uses, truncate to the same prefix length, and look the prefix up in the local set; a miss means the URL is safe with respect to that list and can proceed immediately with no network round trip.
- On a prefix hit, the URL may or may not be malicious, so send only the prefix — not the full URL — to the service and receive the set of full hashes sharing that prefix, then compare your full hash against that returned set. If your full hash is present the URL is known-bad and you should warn; if not, it is safe.
- Implement URL variant checking the way the provider's algorithm does, because attackers randomize query parameters: the source says roughly ten to twenty variants are checked, including progressively shortened paths and the site's home page. A reported malicious home page blocks the whole site and forces an attacker onto new domains that cost money to register.
- Verify the current algorithm, prefix length and variant rules against the provider's live documentation before implementing, and log block events for review.
Caveat: This is a blacklist approach and is guaranteed to miss cases — newly registered domains, unseen URLs with unique tokens such as private document links, and dynamic query parameters will not be listed. The source presents this as a trade-off: a whitelist would be unusable for the open web but may suit highly paranoid, narrow contexts.
Caveat: Prefix truncation leaks some information: a provider can learn that you visited a URL matching a given prefix and could correlate requests over time by IP.
Caveat: Always treat safe browsing as an additional layer of defense, not a replacement for browser protections or for your own link and content review.
Caveat: List sources include user reports and automated crawling in sandboxed environments; coverage is not guaranteed and current behavior should be confirmed with the provider.

Tags: bot-and-agent-security, phishing-defense, url-reputation, hashing, upstream-workflows, caching, content-moderation
Source: Site Security (1).docx

---

## Understand side-channel leakage as a class of risk to storefront logic
Use when: You are designing storefront or API logic that must not reveal whether a customer, coupon, account or inventory condition is true — for example email-enumeration checks in password reset, coupon validity endpoints, or stock lookups on a product page.
- Accept the definitional point from the source: a side channel exists when the implementation is correct — no code bug — yet an attacker can learn information they should not, because the system behaves observably differently between cases it is trying to hide.
- Enumerate the observables in your own stack: response time, response size, error text, HTTP status, and the order in which your server performs work.
- Identify secrets whose value is being compared or looked up: whether an email is registered, whether a password guess matched a prefix, whether a coupon code exists, whether a given SKU is in stock at a specific warehouse.
- For each, design the response so the observable is identical in both cases — same status code, same generic message, same approximate duration — and where comparison itself is the secret, use constant-time comparison for secrets such as tokens and password-derived values rather than short-circuiting on the first mismatched character.
- Rate-limit and monitor for repeated near-identical probing patterns, since side-channel extraction works by asking many small questions and observing answers over time.
- Validate on your own environment by measuring response-time variance and comparing response bodies for the true case and false case of each question, then confirm the two distributions are not trivially separable.
- Treat timing variance as noisy: network conditions and server load blur measurements, so a timing difference is a signal to investigate, not proof of exploitability.
Caveat: The source's vivid examples — recovering speech from high-speed video of a chip bag or plant leaves, and extracting keys from power-line monitoring — are research results in physical settings; they illustrate the general principle, not a threat model for an online store.
Caveat: Do not present constant-time comparison, uniform error messages or rate limiting as a guarantee against all side channels; they remove specific observables.
Caveat: Measurement-based validation on shared infrastructure is approximate and should not be treated as a certified threshold.

Tags: bot-and-agent-security, side-channel, timing-attack, api-security, customer-accounts, measurement, privacy
Source: Site Security (1).docx

---

## Browser history disclosure via CSS :visited and the whitelist trade-off
Use when: You are reviewing a storefront's CSS or third-party scripts embedded on PDP, checkout or content pages, and deciding whether any styling rule could reveal a visitor's prior browsing behavior to that page.
- Understand the historical vulnerability: browsers rendered visited links in a different default color than unvisited links, and scripts could read a link's rendered color to determine whether the visitor had been to a URL. Enumerating a large array of URLs would reveal the visitor's interests and history.
- Recognize that the leak is not limited to color: the source notes CSS can also load a background image from an attacker's server when a link is visited, giving the attacker a server-side request as the signal, and can alter a visited link's position or size, which JavaScript can detect via layout changes.
- Note the attempted alternatives and why they were rejected: only marking visited when the user clicked from that same site was considered but dropped for usability reasons because users would be confused by inconsistent styling, and simply making the color unreadable does not address the other CSS channels.
- Apply the principle of the 2010-era mitigation: restrict the set of CSS properties that can apply to :visited links to a small whitelist of text-level changes such as color, underline, bold and italic, removing background images, positioning and sizing so layout-based detection is impossible.
- Apply the accompanying performance-based defense: slow down the rate at which a page can probe history, making bulk enumeration impractically slow rather than impossible — the source frames this explicitly as accepting that the issue cannot be fully fixed and raising the attacker's cost instead.
- For your own storefront, audit every third-party script and stylesheet on customer-facing pages for use of :visited selectors and layout-changing rules, and remove or isolate anything that reads computed styles of links.
- Verify the current browser implementations rather than relying on the historical description — modern browsers continue to restrict :visited styling, so check current behavior before assuming a specific fix.
Caveat: The source describes a 2010 change, attributed in the lecture to Mozilla/Firefox; browser behavior has evolved since, so treat the specific implementation as historical context and verify the current state.
Caveat: This is a privacy leak of browsing history, not a data breach of your store's own records; the primary harm is to visitors.
Caveat: Style restrictions do not make visited-link state invisible in principle — they reduce the channels through which it can be read.
Caveat: Do not claim that removing a selector or a script guarantees no history disclosure, since other techniques may exist.

Tags: bot-and-agent-security, privacy, css, browser-security, third-party-scripts, content-security
Source: Site Security (1).docx

---

## Secure handling of retrieved documents and tool output in agent workflows
Use when: You are deploying an ecommerce automation agent that reads supplier pages, review content, uploaded CSVs, order notes or API responses and then acts — for example updating prices, drafting replies, creating orders or running scripts.
- Classify every input the agent processes into trusted configuration versus untrusted content, where untrusted includes scraped pages, user-uploaded files, email bodies, third-party API responses and any tool output that carries external text.
- Define the agent's permitted scope explicitly by brand and task — which store, which tables, which tools, which files — as configuration the model cannot alter from content it reads.
- Never let instructions found inside retrieved content change the target, destination, data range or command that will be executed; if a document appears to contain directives, treat that as content to report, not to obey.
- Restrict tool permissions to the minimum needed for the task: read-only query access where writes are not required, an allowlist of programs the automation may run, and no shell string construction from fetched values.
- Require human approval for irreversible or high-impact actions such as bulk price changes, refunds, order cancellations, credential changes or any operation that deletes data, and log the approval with the actor identity.
- Handle secrets outside of content: keep API keys and database credentials in a secret store that the agent can use through a scoped interface but cannot read back into its context or write into a file, and rotate them on a schedule.
- Log every tool invocation with the requesting identity, the exact parameters, the retrieved content hash and the outcome, so an anomalous action can be traced and replayed.
- Validate on a staging store by feeding a document containing injected directive-like text and confirming the agent takes no action outside its configured scope and instead surfaces the anomaly.
Caveat: Do not claim that prompt filtering, a WAF or content sanitization alone guarantees safety against injected instructions in retrieved content.
Caveat: Distinguish authorization from data handling: seeing a credential or an instruction is not permission to use it, and encryption protects data at rest or in transit, not the decision to act.
Caveat: This card adapts the source's injection principle to agent inputs; the source does not present an agent-specific benchmark or outcome.

Tags: bot-and-agent-security, agent-tools, prompt-injection, least-privilege, approvals, secret-management, logging
Source: Site Security (1).docx

---

## Visited-Link History Leaks and Storefront Fingerprinting Risk
Use when: Auditing storefront or marketing-site third-party scripts and ad pixels for the risk that they fingerprint visitors' browsing history, or advising engineering on what a page's own rendering performance reveals about customer behavior.
- Understand the core vulnerability: browsers apply a 'visited' style to links a user has clicked before, and though the page cannot read the true computed color of a visited link, it can measure how long the browser takes to render or reflow when a link's state changes.
- Recognize that browsers restricted visited-link styling to a small whitelist (color, underline, bold/italic), equalized internal code-path timing, and made style-querying APIs lie (return the unvisited color) — but these are incomplete, so don't assume visited-state is fully protected.
- Treat any third-party script on your PDP, category, or landing pages as a potential timing side-channel: a script can swap an anchor's href between a never-visited made-up URL and a target URL and time the redraw via requestAnimationFrame, using a large text-shadow and thousands of links to amplify the signal.
- Assess the practical risk for a store: leaking which product, category, or competitor URLs a visitor has seen enables cross-site behavioral profiling and targeted phishing; weigh it against the ad/analytics value of the script.
- For your own first-party pages, keep third-party JS minimal and audited in checkout and account flows, where a history leak plus a credential-capture page is most damaging.
- Verify current browser mitigations before acting: behavior described here is implementation-specific (notably Chrome) and changes over time, so re-test rather than relying on a fixed rule.
Caveat: The timing technique is unreliable — the source's demo had false negatives (a visited link measured below threshold) though no false positives; enlarging the shadow was only a hypothesis for improvement.
Caveat: This is a fundamental, hard-to-fully-fix client-side problem; there is no complete mitigation, so scope decisions to risk reduction, not elimination.
Caveat: Do not assume any single browser mitigation (CSS whitelist, timing equalization, lying APIs) prevents all leaks — the source explicitly calls the solution incomplete.

Tags: bot-and-agent-security, fingerprinting, third-party-scripts, privacy, customer-research, frontend-security
Source: Site Security (1).docx

---

## Cross-Site Image Requests and Cookie-Bearing Side Channels
Use when: Reviewing cookie attributes, third-party image embeds and account-state endpoints on a storefront, or threat-modeling how a competitor or attacker page could learn whether a customer is logged into your store or payment/email accounts.
- Understand the mechanism: when a page loads an image from another origin, the browser automatically attaches cookies for that origin, and the response can vary (e.g. a 'log in' vs 'log out' button of slightly different width) based on those cookies.
- Recognize that the embedding page cannot read the foreign image's pixels or cross-origin state, but can still infer it: differences in image dimensions can shift layout, which attacker JavaScript detects; the attacker can also just observe the rendered size.
- Prevent it for your own store by setting same-site cookies (SameSite) on session and authentication cookies so they are not attached to requests initiated from other origins, which forces the cross-site request to look signed-out.
- Audit any state-dependent images or endpoints (login buttons, feature flags, personalized banners) that return different content for logged-in users and are embeddable cross-site, since these are the exploitable surfaces.
- Also treat sensitive images (e.g. QR codes containing keys) as leakable via side channels: because image dimensions/position are observable, avoid serving secrets as embeddable images without origin restrictions and auth checks.
- Verify the current cookie defaults and SameSite behavior in target browsers before assuming protection, since defaults have changed over time.
Caveat: There is no general way around the underlying information leak from image size/layout; SameSite cookies solve the cookie-attachment variant but not all size-based inference.
Caveat: This is described as an unintentional leak violating the spirit of the same-origin policy, not a designed feature to rely on.
Caveat: Exact browser cookie-default behavior is version- and vendor-dependent; confirm rather than assume.

Tags: bot-and-agent-security, cookies, same-site, session-security, account-security, privacy
Source: Site Security (1).docx

---

## Ambient-Light Sensor as a Browser-History and Image-Reading Side Channel
Use when: Deciding which browser sensor/permission APIs to allow or request on a storefront or PWA, or assessing privacy exposure of device-sensor features used for theming, games or interactive PDP experiences.
- Understand the attack: a page can render content (e.g. a link with a black background if unvisited, white if visited, or a QR code region) and read the ambient-light sensor value (0–1) to infer what is on screen.
- Calibrate first by showing a fully white page then a fully black page and reading the sensor each time; then render the target and infer its color from the sensor value against those two reference readings.
- Recognize the image-reading variant: because a QR code (or any sensitive image) loads cross-origin with cookies but cannot be read as pixels, an attacker can zoom the display into one cell at a time and read black vs white via the sensor, reconstructing the whole image.
- For your store, avoid using sensor-gated features that could be repurposed; if you add light-adaptive theming, know that fine-grained ambient-light access can silently expose on-screen content.
- Mitigations to consider: request sensor access behind a permission prompt, limit the frequency of sensor reads, and quantize sensor precision so a site cannot extract high-resolution signal.
- Check your target browsers: this API's shipping status and permission model were under reconsideration at the time of the source, so verify the current interface before building on it.
Caveat: The demonstrated attacks are described as technically real but low-practicality (they occupy the screen and are visible to the user); practicality doesn't remove the policy violation.
Caveat: Browser vendors were reconsidering whether to ship the ambient-light API unpermissioned — availability and protection status must be verified and may differ per browser.
Caveat: Restricting these APIs also breaks legitimate demos and features; treat this as a security-vs-capability tradeoff, not a free win.

Tags: bot-and-agent-security, sensor-apis, browser-privacy, fingerprinting, permissions, product-page
Source: Site Security (1).docx

---

## Gyroscope API Eavesdropping and Sensor Permission Tradeoffs
Use when: Deciding whether a storefront, web game or interactive product experience should request motion/orientation sensor access, and auditing which sensitive device-permission APIs your site invokes.
- Understand the 2014 Stanford finding: the gyroscope API could be precise enough to pick up acoustic signals so a site without microphone permission could infer what was being said near the device.
- Recognize the general pattern — any unpermissioned, high-precision sensor (motion, ambient light, etc.) can be repurposed as a covert input channel and a privacy leak.
- For your store, avoid requesting motion/orientation access unless a specific interactive feature genuinely needs it, and explain why when you do; users who grant access for a game are also granting whatever else the site does with the data.
- Accept that once a user has granted a permission, you cannot reliably control how the data is subsequently used — the same concern applies to native apps that use granted navigation/location data for ad targeting.
- Mitigations for platforms/your own features: gate sensors behind permissions, limit reading frequency and quantize precision to reduce the extractable signal.
- Verify current platform state: iOS moved the gyro API behind a permission flag (reported around iOS 12/13), so check the present OS/browser behavior before relying on it.
Caveat: Locking down sensor APIs breaks legitimate orientation-based experiences; this is an explicit security-vs-capability tradeoff.
Caveat: The eavesdropping demonstration was a research result, not a promise that arbitrary sites will succeed against modern devices — precision and OS gating affect feasibility.
Caveat: Permission prompts do not fully solve the problem, because users may grant access for one purpose and the data may be used for another.

Tags: bot-and-agent-security, sensor-apis, permissions, browser-privacy, native-apps, privacy
Source: Site Security (1).docx

---

## Why Side Channels and Phishing Resist Full Mitigation
Use when: Setting realistic security expectations for a storefront — deciding how much engineering effort to spend on browser-level hardening versus user education, monitoring and account controls.
- Treat side channels as an inherent, ongoing class of leak rather than a single bug: timing, layout, image-size and sensor channels each need separate analysis, and fixing one doesn't close the others.
- Treat phishing as a human problem: a phishing page becomes more effective when it first learns (via a side channel) which service the victim uses, so reducing pre-click information leaks also reduces phishing success — but no single control eliminates phishing.
- Accept the security-vs-capability tension: every restriction that closes a side channel (banning link styling, gating sensor APIs) also breaks legitimate features, so design controls to target the highest-risk leaks rather than blanket bans.
- For a store, combine layered defenses: minimal third-party scripts, SameSite session cookies, MFA and login-anomaly monitoring, and clear customer communication about how your store contacts them.
- Distinguish login/session security from data-leak concerns when prioritizing, and don't expect any one mitigation (HTTPS, CAPTCHA, a WAF or prompt filtering) to guarantee safety against these classes.
- Re-verify browser mitigations over time, since vendor behavior is implementation-specific and changes as standards evolve.
Caveat: Side channels are described as fundamentally hard, if not impossible, to fully prevent — plan for risk reduction, not elimination.
Caveat: Phishing success depends on user behavior and cannot be fully engineered away.
Caveat: Do not assume any single control guarantees security; treat each as one layer among several.

Tags: bot-and-agent-security, phishing, side-channels, defense-in-depth, risk-management, account-security
Source: Site Security (1).docx

---

## Command Injection in Store Backends and the Argument-Array Fix
Use when: Reviewing or writing any store backend code or admin/integration feature that shells out — file viewers, image/asset processing, export tools, report generators or third-party CLI wrappers.
- Understand the vulnerability condition: whenever code concatenates untrusted input (URL params, form fields, cookies, headers) into a shell command string, a special character such as a semicolon can terminate the intended command and start a new one the attacker controls.
- Recognize that untrusted data reaches the shell wherever the client can influence a value — query strings, form bodies, cookies — so treat all of it as attacker-controlled.
- Fix it by using a spawn-style API (e.g. Node's spawnSync, with equivalents in Python, Ruby and others) that takes the program name and an explicit array of arguments, so the library escapes each argument and guarantees only the intended program runs.
- Avoid the insecure pattern (e.g. exec with a concatenated string); the safe pattern passes arguments as a list and returns a child-process object, so read stdout on success and stderr on non-zero status.
- Note that escaping user input fixes command injection but does not fix other flaws: a file viewer that lets users choose any path still allows path traversal (e.g. ../../etc/passwd), so also restrict which files are accessible.
- Verify the exact function signatures and return shapes in your language, since the API details differ and may change across versions.
Caveat: Escaping input prevents adding commands to your program but does not prevent the program itself doing something dangerous with a valid-looking input (e.g. reading arbitrary files).
Caveat: The source's live demo ran on the presenter's local interface only; do not reproduce injection tests against systems you don't own or have written authorization to test.
Caveat: Exact function behavior (return value, escaping rules) is language- and version-specific — confirm against current docs.

Tags: bot-and-agent-security, command-injection, input-validation, backend-security, integrations, code-injection
Source: Site Security (1).docx

---

## Review store database queries for SQL injection
Use when: Reviewing authentication, search or account-lookup endpoints on a store for SQL injection, or testing whether an input field safely parameterizes queries.
- Trace customer input and imported data into database query construction.
- Use parameterized queries for values and allowlisted mappings for dynamic identifiers; avoid concatenation.
- Use harmless fixtures in an owned test environment to confirm unusual input is treated as data.
- Inspect query errors without interpreting every syntax error as proof of injection.
- Apply least-privilege database access and review adjacent endpoints using the same query helper.
Caveat: No visible error does not prove a query is safe; code review and bounded validation are complementary.

Tags: bot-and-agent-security, sql-injection, input-validation, authentication, backend-security, code-injection
Source: Site Security (1).docx

---

## Stacked SQL Injection via APIs That Allow Multiple Statements
Use when: Choosing database query APIs for a store backend and reviewing existing endpoints that run SQL for login, logging or admin operations.
- Understand the condition: if the injection point sits in code that uses an API allowing multiple statements (e.g. an exec-style call), an attacker can terminate the intended query with a semicolon and append a second one.
- Recognize the impact: an appended query can update another user's password (then log in as them), insert attacker data, or drop an entire table — the source demonstrated both password takeover and dropping the users table.
- Note that some APIs (e.g. a get-style single-row fetch) reject multiple statements, so a payload that fails there may still succeed elsewhere in the same app — audit every query call site, not just one.
- Watch realistic second-statement surfaces: any feature that runs an extra query on the same code path (such as inserting a login-attempt log row) can become the vector that enables stacked statements.
- Remediate by using parameterized queries everywhere and by selecting database APIs that disallow multiple statements in a single call where possible; never concatenate user input into query strings.
- Verify current behavior of your specific driver/library, since multi-statement support and defaults vary by engine, driver and version.
Caveat: Protection against stacked queries depends on the API and database; a fix in one call path does not protect another.
Caveat: The demonstrated password change and table drop are examples of impact, not guarantees that every injection yields them.
Caveat: Do not test destructive payloads against systems you don't own or lack written authorization to test.

Tags: bot-and-agent-security, sql-injection, backend-security, database-security, input-validation, code-injection
Source: Site Security (1).docx

---

## Recognize blind SQL injection signals without exposing customer data
Use when: Assessing whether a store endpoint that accepts search/filter input and gives only success/failure or timing feedback could leak database contents, and prioritizing remediation for such endpoints.
- Review repeated unusual parameter probes, response differences and timing anomalies affecting store data endpoints.
- Trace suspect inputs to query construction and parameterize the underlying values.
- Use synthetic records and bounded tests in an owned test environment to validate the fix; do not extract real customer records.
- Keep error messages generic while retaining useful restricted diagnostic logs.
- Use least privilege and query/resource limits as additional containment, not a replacement for parameterization.
Caveat: Timing differences can have benign causes; confirm the root cause before declaring exploitation.

Tags: bot-and-agent-security, sql-injection, blind-injection, backend-security, measurement, code-injection
Source: Site Security (1).docx

---

## HSTS: force browsers to HTTPS and rewrite HTTP requests
Use when: You are hardening checkout, login and account pages against network interception, and deciding an HSTS rollout plan for your storefront domain.
- Serve the Strict-Transport-Security response header from your store; browsers will then internally rewrite HTTP requests for that host to HTTPS before they hit the network, and will not offer users a click-through on certificate errors for that site.
- Set the max-age directive to the cache lifetime. When first testing, use a very low max-age so you can back out; mature deployments move to long values (the speaker cites around a year as a cap).
- Use includeSubDomains only after auditing every subdomain, because it applies to all of them — the source notes large organizations get stuck when one vendor-operated subdomain lacks HTTPS.
- Because a subdomain cannot set HSTS for the whole registered domain, if users land on www.example.com, load an invisible first-party resource from example.com that carries the includeSubDomains header.
- Submit to the preload list only when you are committed long-term: preloading fixes the vulnerable first-visit gap but removals are slow and bottlenecked on browser release cycles.
Caveat: HSTS is effectively irreversible once cached by real users — there is no undo, which is why gradual max-age increases are recommended.
Caveat: The first visit is still unprotected unless your domain is on the browser preload list.
Caveat: HSTS state can be abused as a tracking/supercookie vector in third-party contexts; HTTPS and HSTS do not guarantee safety on their own.

Tags: bot-and-agent-security, checkout, account-security, encryption, transport-security, hsts, storefront-hardening
Source: Site Security (1).docx

---

## Recognize HSTS as a persistent third-party tracking vector
Use when: You are assessing third-party scripts, pixels or ad-network embeds on product and checkout pages for privacy and tracking exposure, or responding to a data-subject request to clear tracking state.
- Understand the mechanism: a third-party script sets HSTS on many unique subdomains to encode an identifier in bits, then reads it on other sites by detecting which sub-resource loads are upgraded to HTTPS.
- Treat any persistent per-browser state that can be set and read in third-party contexts as a potential tracking vector, not only cookies.
- Recall that HSTS state is not cleared by clearing cookies — a user (or your own QA) may believe they started fresh while persistent state remains.
- Audit which third parties load sub-resources on your store templates and reduce the number of distinct third-party origins, especially on payment and login flows.
- When evaluating browser protections, prefer the stable principle (limit third-party state) over current vendor-specific rules, which change; verify the current behavior in each target browser before relying on it.
Caveat: The source describes Apple/Safari and Chrome mitigations as evolving and states Chrome's plan was not final at the time; do not treat any specific vendor rule as a permanent guarantee.
Caveat: Prevention is described as a trade-off between security and privacy, not a solved problem.

Tags: bot-and-agent-security, privacy, customer-research, third-party-scripts, tracking, hsts, measurement
Source: Site Security (1).docx

---

## Treat HTTPS as baseline, not a proof of trustworthiness
Use when: You are deciding what security claims to make on your storefront landing page or checkout (badges, trust copy) and which protections to actually implement.
- State the real properties HTTPS gives: confidentiality, integrity and authentication of the server over TLS — and that it does not by itself validate the merchant, the content, or the product.
- Account for the certificate bottleneck: any certificate authority can issue for any domain, so a compromised or fraudulent CA can impersonate your store to users on the attack path.
- Do not stop at redirecting HTTP to HTTPS: an attacker on the network can strip the redirect and inject content, so serve HSTS rather than relying on redirects.
- Prefer controls that are checkable and auditable (CAA DNS records, certificate transparency monitoring) over claims that cannot be verified, and describe them accurately.
- If you use a hosted platform (hosted CMS, cloud web server), confirm whether it enables HTTPS/HSTS for you by default and what you still need to configure yourself.
Caveat: Positive security indicators such as lock icons were found by research cited in the source to be unreliable — users generally do not notice a missing indicator.
Caveat: The source notes HTTPS adoption lagged in some regions historically and migrating large existing sites remains technically challenging.

Tags: bot-and-agent-security, encryption, pdp, checkout, trust-signals, certificates, transport-security
Source: Site Security (1).docx

---

## Use CAA DNS records to constrain who may issue certificates for your domain
Use when: You are setting up or reviewing domain-level certificate management for your storefront and want an implementable control against mis-issuance.
- Publish a CAA DNS record listing the CA(s) you actually use, so a CA checking before issuance sees it is not authorized and should stop.
- Treat CAA as advisory enforcement: it relies on CAs behaving correctly, and remediation is after the fact (revocation, escalation) rather than runtime prevention.
- Understand the gap: DNS itself was not integrity-protected or authenticated at the time of the source, so an on-path attacker between CA and your DNS could tamper with the response; the source treats it as better than nothing, not a guarantee.
- Pair CAA with certificate transparency monitoring to detect issuance you did not request.
- Keep records current when you change issuers, since a stale CAA record can block legitimate renewal.
Caveat: CAA does not stop a determined or compromised CA from mis-issuing.
Caveat: CAs generally do adhere, but this is behavioral, not cryptographic enforcement.

Tags: bot-and-agent-security, certificates, dns, domain-security, mis-issuance, encryption
Source: Site Security (1).docx

---

## Treat browser certificate pinning as deprecated and use the alternatives
Use when: You are evaluating whether to implement HPKP or certificate pinning on your storefront or deciding how to respond to pinning advice from a vendor or agency.
- Do not plan new adoption of dynamic HPKP: the source states Chrome unshipped it years after launch because server operators could not reliably predict the chain a client would build, and failures were unrecoverable and non-actionable for users.
- If you still have HPKP configured, remove it and rely on safer mechanisms; a wrong pin with a long max-age can lock users out of your site even after you recover from an incident.
- Make sure any pinning you do pin public keys, not serial numbers or other certificate fields — the source calls non-key pinning forgeable and incorrect.
- Prefer CAA records plus certificate-transparency monitoring as your primary mis-issuance defense; understand both are after-the-fact/audit-based rather than runtime prevention.
- Recognize hostile pinning as a risk: an attacker who compromises your server could set pins that brick access to your domain.
Caveat: The source notes some operators were unhappy to lose pinning's safety benefits and were using hostile pinning as a feature; removal was a deliberate trade-off, not a claim pinning never helps.
Caveat: Static preloaded pins still exist in Chrome for a curated set of high-value sites, but are not something a typical merchant can self-serve quickly.

Tags: bot-and-agent-security, certificates, encryption, tls, mis-issuance, vendor-evaluation, deprecated-technology
Source: Site Security (1).docx

---

## Plan HSTS preload carefully: it fixes the first-visit gap but is slow to reverse
Use when: You are deciding whether to submit your storefront domain to the HSTS preload list and how to sequence that decision.
- First recognize the gap you would be closing: without preload, the very first visit to your site is unprotected because the browser has not yet received your HSTS header.
- To prove domain control for preload, serve the HSTS header with the preload directive on the site — that is the ownership proof mechanism described.
- Meet the list's automated requirements, then submit via the public preload site; note that Chromium maintains the list and other browsers apply their own policies on top, so removal may take even longer.
- Know the reversal cost before committing: removal could require waiting on a release cycle for Chrome and potentially longer for other browsers.
- Do not submit expecting to check the site's ongoing health: the source says entries were not pruned for liveness at the time.
- Weigh the binary-size cost context: on Android, larger browser binaries can mean a percentage of users do not get updates, and users may pay for the download data.
Caveat: The preload list was originally intended for a small set of high-value sites and grew into an unsustainable general list, per the source.
Caveat: Verify the current preload submission and removal process, as the interface and policies may have changed.

Tags: bot-and-agent-security, hsts, transport-security, certificates, release-management, storefront-hardening
Source: Site Security (1).docx

---

## Track your HTTPS/HSTS adoption as a migration metric
Use when: You are migrating a legacy or large storefront to HTTPS/HSTS and need to sequence the rollout without breaking customers.
- Start with short HSTS max-age values to test, then increase toward long values once confident; the source specifically warns against jumping straight to a one-year expiration.
- Before enabling includeSubDomains, inventory subdomains and any vendor-hosted services; domains without HTTPS support will block you from enabling it across the whole domain.
- To cover a registered domain from a www landing page, use the first-party sub-resource trick described (an invisible resource loaded from the apex carrying includeSubDomains).
- Expect breakage when disabling insecure subresources: the source describes running experiments for an extended period and measuring breakage before phasing out mixed content.
- Keep the old HTTP behavior available while measuring, then deprecate it deliberately — the source frames platform changes as breaking things carefully on the platform's terms.
Caveat: The specific timelines in the source are historical and may not match current browser behavior; verify against current documentation.
Caveat: Not all environments can migrate at once — hosted platforms may enable HTTPS for you, while large custom deployments remain harder.

Tags: bot-and-agent-security, hsts, transport-security, migration, measurement, release-management, mixed-content
Source: Site Security (1).docx

---

## Harden mixed content by eliminating HTTP subresources on HTTPS pages
Use when: You are auditing product, category and checkout templates for insecure subresource loads (images, scripts, fonts, pixels) and planning remediation.
- Inventory every subresource loaded by your templates and flag any absolute http:// URLs, hard-coded HTTP links and HTTP-scheme embeds.
- Convert them to HTTPS or same-origin resources; verify the source actually serves HTTPS, and re-test after each batch rather than flipping everything at once.
- Treat the known trade-off: the source states that when a page is already served over HTTP and loads an HTTP subresource, HSTS will not be applied — you lose the upgrade on those loads.
- If you sponsor or operate vendors/ad networks, require HTTPS subresource delivery in your contracts and audit their scripts, since insecure third-party scripts can be replaced with malicious content (the source cites a real-world case of analytics scripts loaded over HTTP and swapped in transit).
- Run the migration as a measured experiment: the source describes a multi-year measurement phase and a staged timeline rather than a single cutover.
Caveat: Legitimate HTTP links will stop working, and the source acknowledges the change causes breakage.
Caveat: Browser behavior around mixed content autoupgrading has evolved; verify current behavior in your target browsers before relying on it.

Tags: bot-and-agent-security, mixed-content, transport-security, storefront-hardening, third-party-scripts, checkout, pdp
Source: Site Security (1).docx

---

## Do not trust positive security indicators or geographic CA blocking
Use when: You are deciding how to communicate security to shoppers or being asked to approve a 'block by country/region' style control for your store or infrastructure.
- Do not rely on users noticing a missing lock icon: research cited in the source shows positive security indicators are not a reliable signal, so treat visual trust badges as reassurance copy, not a control.
- Reject 'just block a region or country' as a certificate mis-issuance defense; the source notes issuers serve customers globally and that mis-issuance has come from various geographies, and blocking is unenforceable and hard to define.
- If a vendor proposes region blocking as a security or anti-fraud measure, ask what specific threat it addresses and what false-negative rate it creates for legitimate international customers.
- Invest effort instead in controls that apply to all traffic: TLS/HSTS deployment, CAA records, certificate transparency monitoring and sane third-party script policies.
- If you communicate security claims to shoppers, keep them factual and verifiable rather than relying on user vigilance.
Caveat: The source's remarks on certificate authorities and geography are situated in web-PKI context; regional or IP blocking can still have legitimate, non-security uses such as regulatory controls.
Caveat: This is a strong opinion from the presenter, supported with historical examples rather than a controlled study.

Tags: bot-and-agent-security, certificates, trust-signals, pdp, mis-issuance, fraud-prevention, storefront-hardening
Source: Site Security (1).docx

---

## Keep authentication, authorization, encryption, hashing and signing distinct in store design
Use when: You are specifying security requirements for storefront accounts, payment integrations, agent credentials or admin access and need to state each control precisely.
- Separate the properties: TLS/HTTPS provides confidentiality, integrity and authentication of the server; hashing (like the SHA-256 used for pinned keys) is one-way and verifies material, not identity by itself.
- For server identity, the relevant control is certificate validation against a trusted chain — not the lock icon and not the mere presence of HTTPS.
- For integrity of a DNS-based control such as CAA, note that DNS is not integrity-protected in the source's account, so the control is advisory.
- Apply the same discipline to store accounts and bot defense: do not describe CAPTCHA, a WAF or a prompt filter as guaranteeing security — none of them alone is a guarantee.
- Write requirements as testable statements (which property, which mechanism, which failure mode) so engineering and vendor claims can be checked.
Caveat: The source's specifics about SHA-256 pinning and HPKP describe a deprecated mechanism; the general distinction between key pinning and certificate/serial pinning remains valid.
Caveat: Current algorithm and protocol guidance changes; verify against current standards before implementing.

Tags: bot-and-agent-security, encryption, authentication, certificates, account-security, checkout, requirements
Source: Site Security (1).docx

---

## Treat agents' retrieved documents and tool output as untrusted data
Use when: You are building or reviewing an ecommerce agent that reads supplier documents, product feeds, customer messages or web pages and can then call tools like price updates, refunds or order changes.
- Classify every inbound artifact — supplier PDFs, emails, catalog feeds, support tickets, scraped pages — as untrusted data; agent instructions come only from your own configuration and authorized operators.
- Scope tool permissions to the specific store and task: an agent handling product descriptions should not hold refund or pricing-write credentials.
- Require explicit human approval for irreversible or high-value actions (issuing refunds, changing prices, modifying fulfillment), with the approval recorded.
- Keep secrets out of agent-visible context: inject credentials at the tool-call boundary rather than embedding them in prompts or documents the agent reads.
- Log tool calls with inputs, outputs, the triggering untrusted source and the resulting action, so a malicious injection can be reconstructed and reverted.
- When content instructs the agent to do something outside the task, treat it as a potential injection attempt and stop rather than comply.
Caveat: No single control — prompt filtering, allowlists or retrieval hygiene — is claimed to guarantee safety; use layered controls.
Caveat: Verify the current capabilities and limits of whichever agent framework you deploy against current vendor documentation.

Tags: bot-and-agent-security, agent-security, untrusted-data, prompt-injection, tool-permissions, logging, checkout
Source: Site Security (1).docx

---

## Bound validation of storefront attacks to systems you own
Use when: You are validating a suspected weakness (timing side channel, credential stuffing, insecure subresource, injection) in your own storefront before remediation.
- Establish written authorization over the exact assets in scope: your domains, staging environments, test accounts and test payment flows.
- Convert observed behaviors into vulnerability conditions you can check — for example, whether an endpoint returns measurably different response times depending on whether a queried condition is true, or whether responses differ based on an attacker-controlled predicate.
- Design validation to confirm the condition and the fix, then verify the fix; do not build reusable extraction tooling against third-party systems.
- Involve engineering early to change the design where possible (constant-time or unconditioned responses) rather than trying to detect the probing.
- Record the finding with timings, parameters and environment so a fix can be regression-tested.
Caveat: Testing systems you do not own or are not authorized to test is out of scope and potentially unlawful.
Caveat: A timing difference observed on your environment may not reproduce on production due to caching, load balancing and network variance.

Tags: bot-and-agent-security, vulnerability-validation, timing-attack, authorization, storefront-hardening, experiment-design
Source: Site Security (1).docx

---

## Assume any certificate authority can issue for your store domain
Use when: You are threat-modeling domain impersonation of your storefront (phishing clones, fake checkout pages) and choosing which certificate controls to deploy.
- Accept the premise: any of the trust-store CAs can issue for your domain, which cuts both ways — you can buy cheap or free certificates from almost anyone, and so can an attacker.
- Layer after-the-fact detection and authorization controls: publish CAA records, monitor certificate transparency logs for your domains, and keep an inventory of who can issue for you.
- Understand the trade-off: after-the-fact controls (CAA, CT) reveal and remediate mis-issuance rather than prevent a certificate from being used at runtime.
- Account for attackers inside the trust path: impersonation is most effective against users on the attacker's network path, so combine certificate controls with HSTS and mixed-content hardening.
- Watch for fake-checkout clones as a business risk independent of your own server security, since a mis-issued certificate makes a clone look legitimate.
Caveat: CAA is advisory and DNS was not integrity-protected at the time of the source, so on-path tampering of the CAA lookup is possible.
Caveat: Certificate transparency is described as auditing, with enforcement handled socially/legally rather than automatically.

Tags: bot-and-agent-security, certificates, mis-issuance, domain-security, phishing, checkout, monitoring
Source: Site Security (1).docx

---

## Expect migration resistance and budget for it
Use when: You are pushing an HTTPS/HSTS or mixed-content cleanup across a large store or multi-brand ecommerce organization with legacy systems.
- Anticipate the standard objections — cost of certificates, performance penalties, effort — and prepare current data; the source notes certificates are now often free or cheap and modern HTTPS can outperform HTTP.
- Prioritize measurement over argument: track adoption percentages and page loads still using the old scheme so you can decide when the old path can be shut off.
- Handle non-expert operators by making the safe option the default where possible — the source points to hosted platforms enabling HTTPS for large numbers of sites at once.
- Plan phased timelines and expect to measure breakage before removing the legacy path rather than declaring a hard cutover.
- Accept that some resistance will not be resolved by evidence and sequence the migration so holdouts do not block the security goal for the rest of the estate.
Caveat: The source's remarks on adoption levels and regional patterns are historical observations, not current benchmarks.
Caveat: Specific performance claims about modern protocols should be verified in your own environment before being used as a business case.

Tags: bot-and-agent-security, migration, transport-security, hsts, stakeholder-management, measurement, mixed-content
Source: Site Security (1).docx

---

## Decide between CA-permissive convenience and stricter issuance assurance
Use when: You are selecting a certificate-issuance strategy or vendor for your store and weighing convenience against assurance.
- Recognize the failed approaches: dynamic pinning was tried and removed because chain building, error recovery and hostile pinning made it unreliable; geographic blocking is unenforceable.
- Choose a detect-and-constrain strategy: publish CAA records, monitor certificate transparency, and enroll in static preload or pin programs only where you can accept the release-cycle coupling.
- If you pursue static pinning, include every issuer in your pin set and be aware that a key change you cannot migrate from can brick your site in Chrome until a new release ships.
- For the storefront, prefer broad compatibility (any reputable issuer) with strong detection over narrow issuer restrictions that create operational fragility.
- Review any agency recommendation to implement certificate pinning with skepticism, given the source's account that the web platform removed the feature.
Caveat: The source presents pinning removal as a deliberate trade-off, noting that pinning works when everything is aligned.
Caveat: Static preload pinning still exists for a curated set of high-value sites; eligibility and process are not self-serve.

Tags: bot-and-agent-security, certificates, mis-issuance, vendor-evaluation, tls, monitoring, deprecated-technology
Source: Site Security (1).docx

---

## Certificate Transparency: Detection, Not Prevention, for Storefront TLS
Use when: Deciding how to monitor for fraudulent or mistakenly issued TLS certificates on your store's customer-facing domains.
- Understand the distinction the source draws: CT is detection, not prevention (unlike certificate key pinning, which aimed to block malicious certs). There is a window where an attacker can use a mis-issued certificate before it surfaces in logs.
- Because any certificate (issued intentionally, accidentally, or maliciously) can be submitted to CT logs by the CA, the site operator, or even crawlers like Googlebot, assume certificates for your domain may appear without your involvement.
- Use CT monitoring as one layer of defense-in-depth: watch public logs for certificates on your domains that you did not request, and treat unexpected entries as a trigger to investigate your CAs and resellers/vendors.
- Treat CT coverage as a noisy-attack deterrent and hygiene tool (the source notes Facebook discovered accidentally issued certs via CT, and CAs have been caught violating requirements) — not a guarantee that malicious certs are blocked.
- Do not rely on CT as your only control; pair it with other transport and authentication protections.
Caveat: CT does not provide the security properties of key pinning; mis-issued certs remain usable for a period.
Caveat: A malicious log could delay or selectively omit certificates, and detection timing is unspecified.
Caveat: The source describes CT deployments as still evolving, so verify current browser/log behavior before depending on it.

Tags: bot-and-agent-security, tls, certificate-transparency, monitoring, defense-in-depth, infrastructure-security
Source: Site Security (1).docx

---

## Authentication vs Authorization: Keep Session Tokens Out of the Permission Business
Use when: Designing login, session, and admin-role handling for a storefront or its backend (customer accounts, staff/admin panels).
- Separate the two concepts: authentication answers 'who is this user'; authorization answers 'what is this user allowed to do' (the source notes NIST stresses authentication does not determine access privileges).
- When you issue a session ID to a logged-in customer, issue an identifier only, then look up their current authorizations server-side on each protected request.
- Avoid handing clients signed tokens that literally encode 'I am allowed to do X' — the source notes you cannot expire or update embedded permissions when rights change.
- Model permissions with an ACL (user → allowed actions) or a capability token (a unique hard-to-guess URL token, like a Google Docs link) depending on the access pattern you need.
- For store admin and fulfillment roles, re-check authorization on the server per request so revoking staff access takes effect immediately.
Caveat: The source presents this as general guidance; exact mechanisms (ACL vs capability tokens) trade off revocation and simplicity.
Caveat: Capability-style URL tokens remain valid as long as the URL leaks, so treat them as bearer credentials.

Tags: bot-and-agent-security, authentication, authorization, session-management, access-control, admin-security
Source: Site Security (1).docx

---

## Username Handling Rules: Case-Insensitive Uniqueness, Preserved Display Case
Use when: Implementing customer account creation and login for a storefront where usernames or display handles are used.
- Enforce that usernames are unique so a second user cannot register an easily-confused variant of an existing account.
- For lookup, normalize the typed username (e.g., lowercase it) and compare against a stored normalized column so logins are not case-sensitive in a way that creates duplicates.
- Add a second stored column holding the user's preferred capitalization and render that version in the UI.
- Reject registration attempts that collide after normalization, not just after exact match.
- Apply the same normalization thinking to any account identifier your admin/fulfillment tooling keys on.
Caveat: The source treats case-insensitive uniqueness as the goal; some systems deliberately allow case-sensitive identifiers — decide deliberately rather than by accident.

Tags: bot-and-agent-security, authentication, customer-accounts, data-modeling, account-takeover, input-validation
Source: Site Security (1).docx

---

## Modern Password Policy: Length Over Complexity, Breach-List Checks, No Forced Rotation
Use when: Setting password rules for your store's customer accounts or admin logins.
- Stop requiring a mix of upper/lowercase, numbers, and symbols: the source argues 'complex is not necessarily strong' and such rules push users toward predictable patterns like trailing digits.
- Stop forcing periodic password changes and password histories; the source calls three-month rotation outdated advice that yields trivial incrementing.
- Encourage passphrases: multiple words from a large dictionary were shown by the source to yield more entropy than symbol substitution, and are easier to remember.
- Allow long passwords (the source suggests permitting up to ~64 characters) but set a sensible maximum to avoid password-denial-of-service via slow hashing on huge inputs.
- Enforce a minimum length (the source calls 8 characters the bare minimum, and notes even that is low).
- Screen chosen passwords against known breach databases — the source cites this as NIST's current recommendation.
Caveat: Breach-list blocking can reject a user's legitimate existing password if it has ever leaked — a usability/security tradeoff the source acknowledges, so weigh it against how sensitive the account is.
Caveat: The source frames these numeric thresholds as heuristics, not universal law; the entropy claim depends on dictionary size and attacker assumptions.

Tags: bot-and-agent-security, authentication, password-policy, customer-accounts, nist-guidance, credential-stuffing
Source: Site Security (1).docx

---

## Password Handling Mistakes That Break Security and Usability
Use when: Reviewing a login/signup implementation before launch or when auditing an existing storefront's authentication.
- Do not silently truncate long passwords: the source notes bcrypt caps at 72 ASCII characters and requires only 72 bytes of input, so if you allow longer you must hash first or accept truncation ambiguity.
- Do not disable cut-and-paste in password fields — this breaks password managers, which the source calls out as a real security loss.
- Do not set low maximum password lengths for legacy reasons; the source describes banks capping at ~10 characters as an anti-pattern.
- Avoid password hints with tiny answer sets (the source cites an airline whose hint answers were a dropdown of ~8 options, giving roughly a 1-in-8 guess).
- Do not rely on on-screen click keyboards against keyloggers; the source notes screen recording and click interception defeat them while harming usability.
- Allow arbitrary Unicode (including emoji) in passwords, then hash the password before feeding it to length-limited algorithms like bcrypt.
- Never log passwords in plaintext — the source cites incidents where logs captured credentials; scrub auth fields from request logging.
Caveat: The bcrypt 72-byte limit is a specific library behavior; verify your hashing library's limits rather than assuming.
Caveat: Some of these patterns (e.g., max length) may be forced by legacy systems — the source treats them as mistakes to migrate away from.

Tags: bot-and-agent-security, authentication, password-policy, bcrypt, logging, password-managers
Source: Site Security (1).docx

---

## Defending Against Network-Based Guessing: Rate Limiting, Lockouts, CAPTCHA
Use when: Hardening the login endpoint of a storefront or admin panel against automated credential guessing.
- Distinguish the three attacks: brute force iterates passwords against one account; credential stuffing replays username/password pairs from another site's breach (users reuse passwords); password spraying tries a few common weak passwords across many accounts.
- Rate limit authentication attempts by username so no single account gets too many tries in a window.
- Also rate limit by source IP so an attacker cannot spread attempts across accounts.
- When a limit trips, either delay the response (hold the request) or reject with an HTTP error telling the client to slow down.
- Optionally insert a human-verification step (e.g., CAPTCHA) and unblock the user once they pass.
- Because credential-stuffing lists come from real breaches, pair rate limiting with breach-checked passwords and encourage a second factor.
Caveat: The source cites a stress-test assumption of ~1,000 guesses/second as generous for an online attack, but notes it is an assumption, not a benchmark.
Caveat: CAPTCHA is not a strong stand-alone control — the source describes solving farms and cheap solve APIs.

Tags: bot-and-agent-security, authentication, rate-limiting, credential-stuffing, brute-force, captcha
Source: Site Security (1).docx

---

## CAPTCHA Limits: Why Human Checks Alone Won't Stop Bots
Use when: Deciding how much to rely on CAPTCHA to protect signup, login, or high-abuse store actions (e.g., promo-code redemption, inventory hoarding).
- Assume text-based CAPTCHAs are defeatable: the source cites research solving real-world schemes with high accuracy (e.g., reCAPTCHA at 33%, CNN at 51%, Yahoo at 5%) and notes 'over 1% breakage' is considered broken.
- Account for relay attacks, where an attacker forwards your CAPTCHA to other users (e.g., a free-content site) and returns the answer in real time.
- Account for commercial solver APIs, which the source describes as inexpensive (it cites ~$0.50 per 1,000 solves).
- Prefer risk-based/interactive verification that scores behavior (mouse, scroll, IP reputation) over static text challenges, but still treat it as one layer.
- Layer CAPTCHA with rate limiting, anomaly detection, and (for sensitive flows) strong authentication.
Caveat: CAPTCHA vendors and solvers evolve; verify current effectiveness rather than assuming these figures still hold.
Caveat: Interactive/risk-based CAPTCHAs are harder but not proven impossible to bypass.

Tags: bot-and-agent-security, captcha, bot-defense, rate-limiting, abuse-prevention, fraud-prevention
Source: Site Security (1).docx

---

## Offline Cracking Realities Shape Password-Length Guidance
Use when: Choosing minimum password length and hash settings for customer or admin accounts based on how exposed your credential database is.
- Model three scenarios: online attacks (attacker sends login attempts over the network, limited by rate limits and detection), offline on one machine (attacker has a stolen hash database and cracks locally), and offline on a GPU array (the source cites a ~$20,000 rig as cheap for a determined attacker).
- Because offline attacks are far faster than online, assume any leaked hash database will be worked on at high speed — so raise length requirements rather than relying on login throttling alone.
- The source's mapping suggests passwords under roughly 12 characters are at high risk against a motivated offline attacker; treat that as a heuristic to justify longer minimums.
- Note that exhaustive search isn't the only method: attackers also use known-password lists, which the source says can significantly shorten cracking time.
- Since customers reuse passwords, combine length guidance with breach-list checks and a second factor for high-value accounts.
Caveat: The source presents crack-time figures as illustrative assumptions about guessing rates and hardware, not fixed benchmarks.
Caveat: Do not put real passwords into third-party strength/crack-time testing sites, even ones claiming not to transmit them.

Tags: bot-and-agent-security, password-policy, offline-cracking, hashing, data-breach, risk-assessment
Source: Site Security (1).docx

---

## Multi-Factor Authentication: Knows, Has, Is — and Why Biometrics Stay on Device
Use when: Deciding which authentication factors to offer for customer logins and which to require for admin/staff or high-value store actions (e.g., payouts, price changes).
- Classify your factors: knowledge (password/PIN), possession (phone, badge, hardware key, passkey), and inherence (fingerprint, face).
- Combine categories for two-factor authentication — the source uses the ATM example (card you have + PIN you know) — rather than stacking two of the same category.
- Avoid depending on biometrics as transmittable secrets: the source stresses biometric data is not changeable, so if stolen you cannot reset it.
- Follow the on-device pattern the source describes: use local biometrics only to unlock a cryptographic key store, then authenticate with a key, never sending the raw biometric to the server.
- For sensitive store functions, require a second factor rather than merely encouraging it; for low-sensitivity accounts, encouraging it may be proportionate.
Caveat: The source notes uncertainty about what can be extracted from devices with physical access — assume device compromise can threaten local keys.
Caveat: WebAuthn support (the source mentions GitHub adopting it) is evolving; verify current browser and platform support.

Tags: bot-and-agent-security, authentication, multi-factor-authentication, biometrics, webauthn, admin-security
Source: Site Security (1).docx

---

## Fake Security Indicators: Anti-Phishing Images and Positive UI Cues Don't Work
Use when: Evaluating whether any trust badge, security image, or pre-login indicator on your storefront actually protects customers from phishing lookalikes.
- Do not treat a user-selected security image as phishing protection: the source cites a study where ~72% of participants entered their password even when the security image and caption were removed.
- Recognize that attackers can fetch the victim's image dynamically — the source describes looking up a victim's username on the real site and loading the returned image into a phishing page.
- Recall the broader warning from the source: positive UI indicators are often ignored by users, so a badge appearing in a phishing clone doesn't reliably alert anyone.
- Instead, invest in protections the attacker cannot copy: strong authentication (e.g., passkeys/WebAuthn-style origin-bound credentials), breach-checked passwords, and second factors.
- If you run a brand that is frequently spoofed, treat customer education as a supplement, not a control.
Caveat: The source describes these indicators as deprecated and ineffective, acknowledging they may once have helped; effectiveness studies are dated relative to current phishing tooling.

Tags: bot-and-agent-security, phishing, authentication, customer-protection, mfa, usability
Source: Site Security (1).docx

---

## Security-vs-Usability Tradeoffs: Match Friction to the Value at Risk
Use when: Deciding how strict login policy should be for different account tiers in a store (casual shopper accounts vs. accounts with stored payment, payout, or admin access).
- Ask what an attacker gains from the account: the source contrasts a low-stakes account (it cites streaming history) where heavy restriction may not be worth the friction against financial accounts where a second factor should be required.
- Reserve strict controls — mandatory MFA, breach-list rejection, tighter rate limits — for high-consequence functions like payments, refunds, and admin panels.
- Accept that some policies (for example, rejecting any breached password) will block some users who reuse passwords elsewhere; decide whether that tradeoff is right for your service.
- Expect the attacker to know your scheme: the source says to assume the attacker knows your word list or policy, and to remain safe even then — so don't rely on secrecy of the rule for strength.
- Document the policy per account tier so the tradeoff is a deliberate decision rather than an accident.
Caveat: The source's examples of account sensitivity (streaming vs. financial) are its own illustrations, not measured outcomes for any named service.
Caveat: Overly lax policy on accounts with saved payment methods shifts risk to customers and to you.

Tags: bot-and-agent-security, authentication, risk-assessment, password-policy, mfa, usability
Source: Site Security (1).docx

---

## Defense-in-Depth: Assume the Password Is Already Compromised
Use when: Architecting login and account protection for a storefront where credentials commonly leak or get reused across sites.
- Adopt the source's working question — how can we build a system that stays secure when the attacker has the user's password? — as the frame for designing your login flow.
- Layer controls: strong, length-based password policy, breach-list screening, rate limiting, a second factor, and monitoring for anomalous login behavior.
- Because credential stuffing relies on reuse, verify login activity against indicators like new device/geography patterns rather than trusting the password alone (the source's broader security context emphasizes detecting failures rather than assuming none).
- For sensitive actions (changing stored payment details, exporting customer data), require re-authentication or a fresh second factor even inside an active session.
- Treat each layer as fallible on its own; the goal is that no single failure (e.g., a leaked password) becomes a full account compromise.
Caveat: The source gives this as a design principle, not a specific product recommendation; pick concrete controls that match your stack and sensitivity.
Caveat: No single control (password strength, MFA, CAPTCHA) is presented as sufficient alone.

Tags: bot-and-agent-security, authentication, defense-in-depth, account-takeover, mfa, risk-assessment
Source: Site Security (1).docx

---

## CAPTCHA strength is weaker than it looks — treat it as a speed bump
Use when: Deciding how much to rely on CAPTCHA/reCAPTCHA to protect storefront login, account creation, checkout, or admin actions.
- Assume automated solvers can pass a meaningful share of any given CAPTCHA scheme; treat it as one layer, not the gate.
- Because a single widely-used scraper or solver can be pointed at many stores, do not assume your low profile protects you.
- Layer CAPTCHA with server-side controls that do not depend on the puzzle being unsolvable: rate limits, device/IP reputation checks, behavioral signals, and step-up re-authentication for sensitive actions.
- Log how often CAPTCHA is served and how often it fails. Treat spikes in challenge volume as attack traffic, not just as user friction.
- Set your own tolerance: the source used, as an illustrative example, a 1% solver-success threshold for calling a CAPTCHA 'broken'. Do not copy that as a target — use it only to illustrate that low-looking success rates still matter.
Caveat: Solver success rates quoted in the lecture are examples from a specific set of schemes and years, not current benchmarks for any vendor. Verify current vendor and third-party assessments before choosing a scheme.
Caveat: CAPTCHA does not stop credential stuffing once an attacker holds a valid password; pair it with the login-side controls below.

Tags: bot-and-agent-security, bot-defense, captcha, account-security, checkout, fraud-prevention
Source: Site Security (1).docx

---

## Reputation scoring and invisible challenges (modern reCAPTCHA-style)
Use when: Choosing or configuring a bot-mitigation service for login, account creation, checkout, or coupon/inventory abuse on your storefront.
- Understand the model before you deploy: the vendor collects behavioral signals (mouse, scroll), session characteristics, and IP reputation across its whole customer network, then returns a trust score your site uses to allow, challenge, or block.
- Feed the score into a decision, not just a boolean: define separate thresholds for low-risk (allow silently), medium-risk (challenge or step up), and high-risk (block or require re-auth) actions.
- Apply the score to the specific action rather than the whole session — for example, allow browsing and cart edits but challenge at login, address change, and high-value coupon redemption.
- Watch for false positives on privacy-preserving users. The source notes Tor and VPN-heavy traffic tends to look untrustworthy and gets challenged constantly; if you serve such users, expect and measure the friction.
- Keep a fallback path so a vendor outage or an unscoreable client does not silently lock out legitimate customers. Verify current vendor APIs and consoles, which change.
- Do not treat a trust score as proof of identity or as authorization for privileged actions; it is a risk signal only.
Caveat: The lecture describes the general mechanism, not any specific current product. The exact signals, APIs, and no-UI behavior must be verified against the vendor's current documentation.
Caveat: Cross-site reputation inherently penalizes some legitimate users and introduces dependence on a third party seeing your traffic.

Tags: bot-and-agent-security, bot-defense, captcha, fraud-prevention, account-security, measurement
Source: Site Security (1).docx

---

## Step-up re-authentication for sensitive ecommerce actions (sudo mode)
Use when: Designing the admin/customer account flows where you allow changes to saved payment methods, shipping addresses, email/password, or payout/account details.
- Define a short, explicit list of 'sensitive actions' for your store: change password, change email, add/edit shipping address, add/remove a stored card, change payout/bank details, delete account, add an admin collaborator, generate API keys. Treat anything that redirects goods, money, or account recovery as sensitive.
- Require the user to re-enter their password (or complete MFA) immediately before the sensitive action, then put the session into an elevated 'sudo' state.
- Bound the elevation in time — expire the sudo state after a short window so a later request must re-enter. The source describes GitHub dropping the user back out after a while; set a window matching how long a real change takes, not hours.
- Apply this on the server side per action, not just as a client-side modal, since the point is to require the secret even if an attacker already has session access.
- Log every sensitive-action re-auth (who, when, from where) so you can review anomalies.
- Note the secondary benefit documented in the source: this also protects against brief physical access to an unlocked device — someone who grabs a laptop cannot delete the account or change the payout bank without the password.
Caveat: The source is explicit that this is 'not perfect' and does not cover every action — it is defense-in-depth, not a replacement for fixing XSS/CSRF or for MFA.
Caveat: Adding re-auth adds friction; scope it narrowly to actions whose compromise is genuinely costly.

Tags: bot-and-agent-security, account-security, checkout, fraud-prevention, mfa, admin
Source: Site Security (1).docx

---

## Generic error messages to stop account enumeration on login, signup, and reset
Use when: Writing the copy, logic, and status codes for storefront login, signup, guest-checkout account detection, and password-reset forms.
- Identify every place your store discloses account state: login ('no such user' vs 'wrong password' vs 'account disabled'), signup ('that email is already in use'), and reset ('no account with that email' vs 'we sent a link').
- Return one generic message for all failure states: for login use something like a single 'we couldn't log you in' regardless of whether the user does not exist, the password is wrong, or the account is locked/disabled. For reset, use 'if this email exists, we'll send a link.'
- Make sure the HTTP status code and any machine-readable response fields are also identical; the source calls out that differing status codes leak state even if the visible message is the same.
- Apply the same genericization across all entry points — a common mistake is fixing login but leaving signup or reset revealing state, which lets an attacker bounce between them.
- Consider who would benefit from enumerating your customer list. The source's example is a bank where confirmed customers make phishing far more effective; a specialty retailer's customer list can be similarly valuable.
- Measure the trade-off: legendarily, generic messages confuse users who are unsure which email they registered with, so decide based on how sensitive your customer list is.
- If you want the friendlier specific messages, use rate limiting as the primary control instead (see rate-limiting card) so attackers can't enumerate at scale.
Caveat: The source presents this as a trade-off, not a rule: generic messages are worse UX, and some sites deliberately choose specific messages plus rate limiting.
Caveat: Generic messages must be applied to every related flow or the fix is incomplete.

Tags: bot-and-agent-security, account-security, credential-stuffing, checkout, authorization
Source: Site Security (1).docx

---

## Avoid timing side channels in authentication code paths
Use when: Reviewing or writing login/password-check code where a database or service call only happens when the user exists.
- Watch for the anti-pattern: if the user lookup fails you return immediately, but if it succeeds you do extra work (hashing the submitted password and querying a slow remote service), the two responses take visibly different time.
- Rewrite so both the 'user exists' and 'user does not exist' paths perform the same operations — hash the submitted password and run the lookup regardless, then decide validity only at the end.
- Do not rely on thinking alone; the source recommends empirically testing your own system because you cannot assume the database takes identical time. If you measure a gap, add mitigation or eliminate the branch.
- Treat this as a defense-in-depth detail alongside generic messages and rate limits, not as a substitute for them.
- While addressing this, remember the broader point from the source: mitigation has trade-offs, so prioritize where enumeration actually matters (e.g., account recovery or payment flows) rather than over-engineering low-value paths.
Caveat: The source itself admits it does not know how to guarantee a remote database takes identical time; treat timing mitigation as best-effort and validate.
Caveat: Timing differences are only one of several enumeration channels (messages and status codes leak state more easily).

Tags: bot-and-agent-security, account-security, credential-stuffing, measurement, appsec
Source: Site Security (1).docx

---

## Rate limiting authentication attempts — and the shared-IP caveat
Use when: Setting thresholds and locking policies for storefront login, password reset, and signup endpoints.
- Understand the trade-off: rate limiting lets you keep friendlier, more specific error messages while still preventing an attacker from enumerating thousands of accounts, because each attempt costs them time.
- Set thresholds as a rule of thumb an order of magnitude above what you think the most extreme legitimate user would do — not a tight, theoretical limit. This protects users behind shared NAT, corporate networks, and households sharing one IP.
- Account for IP sharing: too-low per-IP limits can block a hundred legitimate users behind one office IP. Prefer limits keyed on account/IP combinations or add per-account limits alongside per-IP ones.
- Monitor for blocks that hit real customers and raise limits when you see them; the source recommends starting generously and adjusting based on observed friction.
- Layer this with reputation and step-up controls so that a single successful credential-stuffing attempt still faces another checkpoint.
- Verify current framework/library capabilities for layered rate keys (account, IP, device) in your storefront platform.
Caveat: The 'order of magnitude above the extreme user' guidance is the source's personal rule of thumb, not a calibrated benchmark; you must test against your own traffic.
Caveat: Rate limiting alone does not stop low-and-slow stuffing from many IPs; combine with reputation scoring and MFA.

Tags: bot-and-agent-security, account-security, credential-stuffing, fraud-prevention, measurement
Source: Site Security (1).docx

---

## Check signup passwords against breach lists (Have I Been Pwned)
Use when: Choosing and enforcing password policy at account creation and password change on your storefront.
- Integrate a breached-password check into signup and password-change flows (the source names Have I Been Pwned as a service that aggregates leaked passwords; GitHub is cited as one site that refuses such passwords).
- Decide the response: hard-reject the password and ask for another, or allow-with-warning. The source leans toward blocking because attackers already have the list.
- Because leaked-password lists are large and attackers can try them against all accounts at once, treat 'is this password in a known breach' as a stronger signal than a simplistic strength meter.
- Consider breach-alert monitoring for your own admin/staff emails so you know when a password they reused elsewhere is exposed.
- Communicate the policy to users so rejected passwords don't feel arbitrary, and offer a password manager or generated passphrase guidance.
- Verify the current API terms, rate limits, and privacy (k-anonymity) options of any breach-checking service before integrating.
Caveat: This doesn't stop an attacker who already has a valid password; pair with MFA and rate limiting.
Caveat: Breach coverage is imperfect — absence from a list is not proof the password is safe.

Tags: bot-and-agent-security, account-security, credential-stuffing, customer-research, signup
Source: Site Security (1).docx

---

## Proactively lock or flag accounts after a breach you're tangentially involved with
Use when: Incident response and ongoing account hygiene for a storefront whose customers reuse passwords across sites.
- Assume a large fraction of any customer base is already in someone's breach corpus; the source's framing is that 'probably yes' most users are affected by breaches somewhere.
- When you discover credentials belonging to your users in a breach, identify impacted accounts and force a password reset or temporarily lock the account with a notification.
- Make password reuse visible in your security stance: encourage unique credentials and make MFA easy to add, not just available.
- Keep a documented process for the 'we got a breach dump' scenario so response is fast rather than improvised.
- For customers calling about suspicious activity, have a recovery path that requires step-up verification (email + a second factor) rather than knowledge-based questions like 'first pet's name,' which the source ranks as weak, guessable factors.
Caveat: Proactive locking creates friction and support load; scope it to accounts actually confirmed in a breach rather than guessing.
Caveat: You will not have visibility into all breaches affecting your customers.

Tags: bot-and-agent-security, account-security, incident-response, retention, fraud-prevention
Source: Site Security (1).docx

---

## Store passwords with a maintained adaptive password hasher
Use when: Designing or auditing how your storefront stores customer and admin credentials.
- Prefer the maintained identity system or framework password hasher over custom cryptography.
- For new implementations evaluate current Argon2id guidance and platform support; retain a planned migration path for legacy bcrypt hashes.
- Let the library manage salts and encoded parameters; a salted fast SHA hash is not a substitute for an adaptive password hasher.
- Benchmark safe cost settings against login capacity, rate limits and current guidance.
- Verify using the library API and rehash on successful login when the stored format needs upgrading.
Caveat: Algorithm requirements can differ by platform or compliance context. Password hashing does not stop credential reuse, phishing or a compromised login endpoint.

Tags: bot-and-agent-security, account-security, encryption, appsec, signup
Source: Site Security (1).docx

---

## Why strong passwords alone fail — and what they actually protect
Use when: Deciding whether to require MFA on your storefront and explaining the value to stakeholders.
- Be precise about coverage: the source states a strong password protects against two things — password spraying/guessing and brute force. Everything else is out of its reach.
- List what it does not stop: credential stuffing (password reused and already breached), phishing, man-in-the-middle, malware keylogging, extortion, and a physical post-it note.
- Because attacker databases are cheap and lucrative — the source cites a paste claiming 32 million accounts for half a Bitcoin — assume leaked credentials will be tried against your store.
- Therefore treat 'require MFA' as the primary control for accounts, and give users frictionless ways to enroll (TOTP, hardware keys, and WebAuthn-style device authentication where supported).
- If requiring MFA for every login is too costly in UX, use the risk-based approach (next cards): require the second factor only for new devices, new locations, or suspicious behavior.
Caveat: The source's framing ('passwords are broken', choose anything) is deliberately stark and comes from the cited Microsoft blog post — treat it as an argument for MFA, not a claim that password hygiene is pointless if MFA isn't available.
Caveat: SMS-based codes are weaker than TOTP/hardware keys; the source uses TOTP as its worked example.

Tags: bot-and-agent-security, account-security, mfa, credential-stuffing, customer-research
Source: Site Security (1).docx

---

## Use risk-based step-up checks without weakening admin authentication
Use when: Designing when to add an MFA prompt in storefront login and account flows without hurting conversion.
- Set baseline authentication requirements by account and action sensitivity.
- Use new-device, unusual-location and abuse signals as inputs to additional verification, not proof of legitimacy.
- Do not let a remembered device or IP alone bypass required admin or sensitive-action authentication.
- Measure false positives for shared networks, VPNs and traveling customers.
- Maintain recovery, session revocation and rate limits alongside step-up checks.
Caveat: The lecture's IP and volume thresholds are examples, not calibrated controls for the store.

Tags: bot-and-agent-security, mfa, account-security, conversion-optimization, fraud-prevention
Source: Site Security (1).docx

---

## TOTP: implementing a two-factor second factor without SMS
Use when: Choosing and implementing a second factor (TOTP/hardware key) for storefront customer and admin accounts.
- On account enrollment, generate a user-specific, cryptographically random secret on the server and store it in a column for that user.
- Deliver the secret to the user's authenticator app — conventionally as a QR code the user scans with an app like Google Authenticator — so both sides share the same secret.
- Code generation: derive a counter from the current time (the source's example uses current time divided by the 30-second interval), run the secret and counter through an HMAC-style function, then reduce the resulting hash to six digits (the source's approach takes a few bytes and mods by 10^6).
- Rotation: the code changes roughly every 30 seconds as the counter increments; the app does this completely offline and never contacts the server.
- Server verification: perform the same derivation using the counter corresponding to the current time and compare with the submitted code; allow a small clock-drift window in practice (verify current guidance from your library, which may differ from the source's raw description).
- Combine with a password so the login requires something the user knows plus something the user has.
Caveat: The shared secret stored on the phone and server is sensitive; losing the device means losing the factor, so provide recovery codes or a second enrolled factor.
Caveat: The exact byte-extraction and drift-window details are implementation specifics — use a maintained TOTP library rather than hand-rolling.
Caveat: TOTP is a second factor, not a replacement for a password, unless you deliberately architect it as a standalone mobile-app-based login (a different design).

Tags: bot-and-agent-security, mfa, account-security, checkout, appsec
Source: Site Security (1).docx

---

## WebAuthn and passkeys: replacing passwords with device-based authentication
Use when: Planning a passwordless or hardware-second-factor login option for customer and admin accounts on your storefront.
- Reduce the phishing problem: the source's core motivation is that passwords are 'terribly fishable' — anyone who convinces you to say your password can replay it exactly. A cryptographic device credential is not replayable this way.
- Model it around a public key: the site holds a public key for the user, and authentication uses a private key that stays on the physical security key or in the device's secure hardware. If the security key is removed, the computer can no longer authenticate on the user's behalf.
- Offer a hardware security key option for high-value/admin accounts, and passkey/biometric options for general customers where the platform supports it.
- Explain to users that the security of 'something you have' rests on the key's hardware protections; a well-engineered hardware key resists even disassembly-style extraction for most threat models.
- Support enrollment and a recovery path for lost keys, and keep a fallback factor so a lost device doesn't permanently lock a paying customer out.
- Verify current browser/platform support and the WebAuthn/passkey implementation details against current documentation — the standard and vendor support have moved on since the source's August launch.
Caveat: WebAuthn shifts trust to the device vendor and platform; it does not eliminate all account-recovery risk.
Caveat: Passwordless isn't a universal fit — many users lack a suitable device or password manager, so the source treats it as an alternative rather than a replacement for everyone.
Caveat: The source's discussion of factor categories is explicitly framed as a design abstraction, noting that not all authentication mechanisms fit neatly into know/have/are.

Tags: bot-and-agent-security, mfa, passkeys, webauthn, account-security, checkout
Source: Site Security (1).docx

---

## Use modern, non-guessable factors instead of knowledge-based questions
Use when: Designing account recovery and verification for storefront customer accounts, billing support, and admin access.
- Recognize the weakness: the source notes that something you know traditionally includes security questions like a first pet's name, which are not tied to anything private and are often externally discoverable.
- Replace knowledge-based recovery challenges with cryptographic factors: registered hardware keys, TOTP apps, or device-bound passkeys.
- For the occasional case where a factor must be something you are — fingerprints, face unlock — recognize that these are device-bound and constrained; use them as the second factor inside WebAuthn rather than raw biometric data.
- Think about threat models broadly: the source raises domestic-abuse scenarios where an attacker technically has the device but the trust boundary should still hold, which matters for recovery and access to sensitive account areas.
- Design recovery so that resetting a factor requires the strongest available proof, not the weakest question, and log the recovery event for review.
Caveat: The source's factor framework is presented as an abstraction that shouldn't be rigidly applied — you ultimately care about keeping the attacker out, not whether a mechanism matches a category.
Caveat: Some users will not have modern device factors; provide a fallback path that is still stronger than a security question.

Tags: bot-and-agent-security, account-security, mfa, customer-research, retention
Source: Site Security (1).docx

---

## Prevent data-breach exposure from common cloud misconfigurations
Use when: Reviewing your store's storage buckets, servers, and database access for accidental public exposure.
- Treat public object storage as your first check: the source notes a common cause of large breaches is simply leaving an S3-style bucket accessible to anyone — anyone with the URL can download everything.
- Assume that once an attacker reaches one application server, they can pivot to databases and other servers reachable from it, so limit network reachability from app servers to data stores.
- Audit for injection classes named by the source (command injection, SQL injection) as entry points that lead to full data exfiltration.
- Include breach response in your operational plan: assume you will be breached eventually, and design so the blast radius is small and detection is possible.
- Because the source's lesson is 'even many well-known companies get breached', do not treat your own competence or obscurity as a reason to skip the audits.
Caveat: This is a general reminder, not a complete audit checklist — many breach causes are out of scope of the source.
Caveat: Assume your customers reuse passwords elsewhere, so even a non-financial breach on your store can enable attacks on other services.

Tags: bot-and-agent-security, appsec, incident-response, fraud-prevention, admin
Source: Site Security (1).docx

---

## Audit your authentication implementation with HIBP and breach-awareness
Use when: Standing up account-security review processes for a storefront, and checking your team's admin/ops accounts for exposure.
- Check admin and support staff emails against the Have I Been Pwned service to discover exposed credentials before attackers do (the source's lecturer demonstrates posting his own email publicly for illustration).
- Subscribe to breach alerts for these emails so you learn about new exposure rather than finding out during an incident.
- Incorporate the same service into your product at password-set time: reject or warn on passwords that appear in known breaches, as discussed elsewhere in these notes.
- Be honest about coverage: the service can only know about breaches that have surfaced publicly, so absence from the list is not a clean bill of health.
- Treat the customer-facing version of this as a way to protect users even when you cannot control their password habits; the source's closing advice is 'protect the user even when the attacker has their password'.
- Encourage password managers so users can generate memorable, unique long passphrases (the source suggests four random words as a memorable, sufficiently random approach).
Caveat: Do not expose or log checked passwords; use a k-anonymity/bulk-check approach and verify the current API's privacy model.
Caveat: The source's 'four random words' advice is offered as an approach, not a formal benchmark.

Tags: bot-and-agent-security, account-security, incident-response, credential-stuffing, customer-research
Source: Site Security (1).docx

---

## Model login security as credential-to-account binding, not factors
Use when: Deciding what login and account-recovery methods your storefront should accept, or auditing why a 'two-factor' customer account can still be taken over.
- List every method your checkout or account system actually accepts as proof of identity: password, email reset link, SMS code, authenticator app code, push notification, security key, biometric unlock, social login, support-desk challenge answers.
- For each, ask the source's test question: if an attacker intercepts or relays that proof in real time, do they gain account access? Email reset links and SMS codes pass that proof along in full, so they collapse to 'as secure as the inbox' or 'as secure as the carrier's number-reassignment process'.
- Note that classic 'something you know / have / are' categories break down (e.g., a security question, a credit-card last-4, an SSH key used only for recovery). Treat these as real factors anyway if your support flow accepts them.
- Rank methods by how recoverable they are for a locked-out customer versus how interceptable they are, then choose a default and a documented fallback.
- Do not convert source opinion (SMS 'really should' go away) into a blanket ban; weigh it against your customers' recovery needs and support cost.
Caveat: The source is a technical talk on authentication, not a study of storefront conversion impact; treat usability trade-offs as judgment calls to test, not measured results.
Caveat: Carrier number-reassignment policy is jurisdiction- and time-specific; verify current practice before relying on SMS as a sole recovery path.

Tags: bot-and-agent-security, authentication, account-security, customer-accounts, fraud-prevention, recovery-flows, measurement
Source: Site Security (1).docx

---

## Attack the password-reset link as your weakest login path
Use when: Designing or reviewing the forgot-password, magic-link login, or email-verification flow on a storefront.
- Trace what a password-reset link actually grants. In the source's description, a single link opened in any browser (even incognito) plus a known username can yield full account access.
- Assume that anyone with access to the linked inbox can take the account; the security of the account therefore equals the security of that mailbox, not the strength of the password.
- If you also require an SMS or authenticator code after the link, check whether the attacker can complete both steps in parallel while the legitimate customer is mid-flow; the source describes attackers racing the customer's own login.
- For storefront admin or high-value accounts (staff logins, payout settings), require a hardware-backed credential or a second independent channel before letting a link alone reset anything.
- Keep an audit trail of link generation so a suspicious reset can be noticed; the source notes customers may spot an unexpected reset email, but attackers who control the inbox can delete it.
Caveat: Requiring hardware keys for all consumer shoppers will cost conversions; scope strict controls to privileged or high-value accounts unless you can measure the trade-off.
Caveat: Email provider security varies; the source's claim that a link equals full account access depends on whether additional factors are required.

Tags: bot-and-agent-security, authentication, recovery-flows, customer-accounts, checkout, account-security
Source: Site Security (1).docx

---

## Recognize anti-phishing images as a non-factor
Use when: Reviewing branded or in-house authentication schemes on your site, or a vendor pitching a custom 'trust indicator' before login.
- Classify the mechanism by asking who it proves: a personal image or pre-set phrase proves the server knows the username, not that the customer is who they claim.
- Simulate the attacker's position: if they sit between customer and server and relay messages in both directions, they forward the server's image to the victim unchanged, so the indicator gives the attacker no obstacle.
- Replace it with transport-level protection (HTTPS) that ties the server identity to something the browser can verify, per the source, rather than a bank-invented scheme.
- If you keep any brand trust cue, do not count it in your authentication or fraud-resistance posture; document it as UX only.
- Do not claim HTTPS or any single control guarantees security; the source presents HTTPS as the real solution to this specific class of relay attack, not as a total guarantee.
Caveat: The source dates this to pre-HTTPS-era banking practice; current browsers and standards may handle these cases differently, so verify what your stack actually does.
Caveat: This card addresses server-impersonation defenses; it does not cover how to detect account takeover after login.

Tags: bot-and-agent-security, authentication, phishing, account-security, customer-accounts, vendor-evaluation
Source: Site Security (1).docx

---

## Rate SMS and app-based one-time codes by interception and phishing risk
Use when: Choosing the default 2FA method for shopper accounts, staff accounts, or a mandatory step at checkout.
- Note the source's assessment: SMS is 'a little bit better than passwords' but has real risks; with moderate effort or money it can be compromised via number reassignment through the carrier.
- Understand the live-race attack: an attacker logging in in parallel with the customer can obtain the same code from an SMS or from an authenticator app the victim is reading; the source warns the moment a user realizes they are being hacked is exactly when they are most likely to type credentials into a phishing page.
- Count the phishing path: a lookalike domain can lure the customer into completing the code exchange with the attacker's server, which then relays it.
- Prefer a hardware-backed credential where possible; the source notes an authenticator app code is no harder to relay than SMS in this scenario, since it is still a typed number.
- If you must keep SMS for conversion reasons, keep it as a fallback rather than the only factor and pair it with anomaly monitoring at login.
Caveat: The source is explicit that sites keep SMS because it is far better than nothing and has a good recovery story for lost phones; a ban is an opinion, not a universal rule.
Caveat: Carrier reassignment protections vary by country and provider and change over time; verify current policy.

Tags: bot-and-agent-security, authentication, two-factor, sms, phishing, customer-accounts, account-security
Source: Site Security (1).docx

---

## Use push-notification login, but read approval prompts carefully
Use when: Evaluating an authenticator-app or push-based login for shopper or admin accounts.
- Confirm the transport: the source contrasts push with SMS by noting it does not rely on SMS network security and goes through secure transports.
- Recognize the residual phish: the customer receives a prompt asking whether they meant to log in to a site, and the source stresses there is no connection between the computer and the approving device guaranteeing the prompt matches the site the customer is on.
- Adopt the mitigation the source cites: some vendors add context such as showing where the login originates so the customer can judge plausibility; treat this as a UX aid, not a guarantee.
- If a provider supports it, prefer requiring a hardware security key for the same flow; the source says it personally does this rather than accept push prompts.
- Train staff/admin users to reject unexpected approval prompts and to report them rather than approving to clear the screen.
Caveat: The source says most of the time push is fine, so this is a risk-trade-off card, not a reason to reject every push-based product.
Caveat: Vendor prompt wording and context features change; verify the current behavior of whichever app you adopt.

Tags: bot-and-agent-security, authentication, two-factor, push-notifications, phishing, admin-accounts
Source: Site Security (1).docx

---

## Design account recovery before you enforce strong factors
Use when: Planning 2FA rollout for shopper accounts or choosing what the support desk may accept to unlock an account.
- Accept the source's framing that recovery is genuinely hard and the compromises are not great; the source attributes the same point to colleagues who push for wider security-key use.
- Choose consciously between two shapes: require multiple independent factors (the source cites sites that require several keys, or SMS/backup codes before adding a key) so losing one is survivable, or permit support-desk verification, which the source warns degrades your physical guarantees.
- If you use a low-risk recovery channel alongside a strong one, state the effective level: a security key plus SMS as backup means the account is only as strong as the SMS path.
- For high-assurance admin access in the style of advanced-protection programs, accept that losing every registered device can lock the account out entirely; document that consequence before enrolling staff.
- Do not present recovery strength as guaranteed: the source calls this unsolved and notes that flexibility means falling back from strong technical measures.
Caveat: The source's own preference is tying recovery to a large trusted platform account (e.g., Apple iCloud Keychain), acknowledging that this just moves the trust problem and carries its own trade-offs.
Caveat: Any support-desk challenge answer you accept should be treated as a real authentication factor in your risk model, even if you call it 'not a factor'.

Tags: bot-and-agent-security, authentication, recovery-flows, customer-accounts, admin-accounts, account-security
Source: Site Security (1).docx

---

## Adopt hardware-backed sign-in and passwordless flows via the browser credential API
Use when: Choosing how to implement security-key or biometric login on your storefront and deciding between passwordless and password-plus-key.
- Model the flow at the API level: the site calls a create operation to register the credential and associate it with the account, then a get operation at login to prove the customer still holds it; the source describes these as the two calls of the browser credential API (verify current names and shapes in documentation, as the argument structures are deep and mix encodings).
- Understand what the site stores: per the source, you save the opaque registration output and later ask a library to validate the returned assertion rather than reasoning about the key material yourself.
- Support username-less login ('passwordlist' in the source) where the device's biometric unlock identifies the customer so they tap once without typing a username or password; the source notes this requires browser support and is bounded by the device.
- Decide on resident (device-bound) keys: the source explains resident key means the credential lives on the physical device's secure element and nothing usable is stored on the server, which supports a stronger assurance for staff logging in from approved hardware.
- Expect real integration cost: the source says it would be hard to recommend this for a service without a dedicated security team, and that library abstractions are the intended path.
Caveat: The source notes the specification is complex and poorly documented in places and that implementations vary; verify the current interface rather than coding to this description.
Caveat: The source says resident-key current behavior can still reveal which usernames a key is registered for, contrary to the spec's privacy goal; do not assume username privacy today.

Tags: bot-and-agent-security, authentication, passkeys, webauthn, security-keys, passwordless, customer-accounts
Source: Site Security (1).docx

---

## Choose between device-bound and synced credentials for shopkeeper and customer logins
Use when: Deciding whether storefront or back-office logins should require a specific physical key versus allowing biometrics synced through a platform account.
- Establish the assurance of the device-bound option from the source: with a resident key, if the device is unplugged or unavailable there is no way to authenticate from another machine, because the only copy of the key is in the hardware.
- Use that for cases where the goal is to guarantee staff sign in only from the tokens your company issued and trusts, which the source gives as the motivating example.
- Weigh the synced alternative the source describes: credentials replicated across a customer's devices through a large platform account, so registering one device and then another lets them authenticate from either, at the cost of trusting that platform's replication.
- Match the choice to the account: high-value administrative or payout access favors the device-bound path; ordinary shopper accounts favor whichever keeps sign-in friction low enough to complete checkout.
- Document the trade-off explicitly rather than defaulting silently, since both options shift who must be trusted.
Caveat: The source presents cross-device credential syncing as emerging ('some indications') at the time of the talk, not an official platform commitment; confirm current support before designing around it.
Caveat: The source's own stated comfort with trusting a platform account is a personal judgment, not a security guarantee for your business.

Tags: bot-and-agent-security, authentication, passkeys, security-keys, admin-accounts, customer-accounts, account-security
Source: Site Security (1).docx

---

## Run authentication as a pluggable abstraction so you can adopt stronger credentials later
Use when: Scoping authentication work on a new storefront or replatforming an existing account system.
- Define one internal interface with two operations in the source's shape: register a credential for an account, and verify a subsequent assertion.
- Keep authentication factors out of your business logic; the source's complaint is that teams spend effort reasoning about which device a customer has instead of simply keeping them secure.
- Store only what the library tells you to store, and delegate validation to it rather than parsing formats yourself; the source notes the wire data mixes several encodings including base64url and array buffers.
- Because the abstraction decouples the site from the specific hardware, you can later add security keys, platform biometrics, or card-based credentials without changing the storefront flow; the source says even exotic options can be layered behind it, including ones requiring manual data transfer between machines.
- Budget for the extra work honestly: the source says implementing this today needs tracking many details unless a good abstraction is in place, and points to open-source abstractions as the mitigation.
Caveat: Do not invent a specific library or vendor recommendation; the source only says an abstraction exists and was open-sourced, without naming it here.
Caveat: Abstraction reduces per-factor work but does not by itself guarantee security; each credential type's threat model still applies.

Tags: bot-and-agent-security, authentication, architecture, webauthn, integrations, customer-accounts
Source: Site Security (1).docx

---

## Check the WebAuthn, CTAP and U2F naming before integrating a device
Use when: Evaluating security-key hardware or browser support while adding key-based login to a storefront.
- Split the layers as the source describes: WebAuthn is the browser-side API the site calls; CTAP is the protocol between the browser and the physical authenticator; FIDO2 combines the browser part with the newer authenticator protocol.
- Treat U2F as the older, formerly non-standard API that WebAuthn replaced, and expect sites and docs to still call security-key registration 'U2F' by legacy naming.
- Verify actual device and browser support before promising customers that keys will work: the source notes a browser that advertises WebAuthn support may in fact only implement the older authenticator protocol, which changes what hardware is compatible.
- Test with the exact browser, OS, and key combinations your customers use, including phone-based keys and app-based unlock, because platform behavior differs.
- When writing customer-facing labels, avoid exposing these acronyms; use a plain term such as a security key for the physical object.
Caveat: Naming and support matrices change as specifications and browsers update; the source's specific compatibility observations are historical and must be re-verified.
Caveat: Do not reproduce the source's confusing acronym mapping as a rule for current products without checking the current spec documentation.

Tags: bot-and-agent-security, authentication, webauthn, security-keys, integrations, vendor-evaluation
Source: Site Security (1).docx

---

## Handle credential-registration privacy between sites
Use when: Reviewing whether your login implementation leaks user identity signals across your own properties or partner sites.
- Verify that per-site scoping is in place: the source states the browser enforces site-unique data so that two sites should find it difficult or impossible to tell that a customer is using the same key.
- Accept intentional within-site detection: the source explains a site is meant to be able to tell when the same key is re-registered, so a customer who accidentally registers twice sees a coherent 'already registered' state instead of a duplicate entry.
- For consumers with no username, note the source's warning that current resident-key behavior can still reveal registered usernames when you probe the device, so username-less login does not yet guarantee anonymity.
- If you operate several storefronts or a marketplace with multiple tenants, treat cross-property correlation as a privacy design decision and document your stance.
- Prefer relying on browser-enforced scoping over custom correlation tricks, and revisit when platform privacy features land.
Caveat: The source describes stronger hardware-trust-reducing protections as work in progress, not shipped features; do not assume they exist.
Caveat: This is about privacy, not authorization; the same protocol does not encode what an authenticated account is permitted to do.

Tags: bot-and-agent-security, authentication, privacy, webauthn, customer-research, compliance
Source: Site Security (1).docx

---

## Value QR-code cross-device login honestly
Use when: Deciding whether to offer scan-to-login on a storefront or in a merchant app.
- Trace the mechanism: the source describes the desktop showing a code, the phone scanning it and communicating to the server that this device has seen the code, usually proving possession with a private key.
- Note the two directions the source distinguishes: logging in from a device that is already authenticated (the desktop is signed in and authorizes the phone), versus scanning while signed in on the phone to log in elsewhere.
- Account for shoulder-surfing and cameras: the code is physically visible on screen, so anyone able to see or photograph it can relay it under some circumstances.
- Recognize the residual phishing risk the source concedes: an attacker imitating the target site can present the code prompt, so this is not immune to the site-impersonation problem.
- Ensure the phone-side gate is strong, since the security of the whole exchange reduces to how well the phone is protected, up to and including a secure element inside the device.
Caveat: The source suggests sites are unlikely to build this going forward if strong credential standards succeed, so treat it as a transitional option.
Caveat: The source's comparison of the two QR use cases is explicitly tentative ('I'd have to take a second to think about how phishable each of those are').

Tags: bot-and-agent-security, authentication, qr-code-login, phishing, customer-accounts, mobile
Source: Site Security (1).docx

---

## Treat client certificates and SSH keys as real factors in recovery
Use when: Auditing ecommerce account-recovery and support processes, or assessing what an integration key can do if exposed.
- Identify the keys you and your customers already hold: on a storefront, that includes SSH or deploy keys used by integrations, and for developer-facing services, the customer's own SSH key used to push or deploy.
- Recognize that the source describes treating an SSH key as an authentication factor in recovery: if a customer has lost their second factors, proving access via the key can be accepted, subject to limits.
- Also count indirect proofs the source cites, such as a device already logged into the account that can be demonstrated to an operator, which functions like a factor for recovery even though it is not part of normal login.
- For your own storefront, map every key or token that can prove account control and decide explicitly whether support may accept it, and under what constraints.
- Because client-certificate UI is annoying and was historically poorly configured, the source notes it never became popular on the public web; keep it for staff or enterprise paths rather than consumer checkout.
Caveat: This describes platform-specific policy at the time of the talk (e.g., certain hosts treating SSH keys as recovery factors) with limits; do not generalize it to any service.
Caveat: Ambient client-certificate authentication carries privacy implications if it identifies users automatically on every visit.

Tags: bot-and-agent-security, authentication, recovery-flows, ssh-keys, integrations, admin-accounts
Source: Site Security (1).docx

---

## Separate authentication from authorization in the credential design
Use when: Scoping account-access requirements for a storefront, a merchant back office, or an agent that acts on a customer's behalf.
- State the split plainly when writing requirements: authentication proves the customer is who they claim; authorization encodes what they are allowed to do (view orders, issue refunds, change payouts).
- Do not expect a hardware key or biometric credential to convey permissions: the source says nothing in this protocol is designed to prove access rights beyond the single key identifying the user.
- Implement permission checks server-side against the authenticated account, and treat the credential only as the identity assertion.
- When an integration or agent acts for an account, bind permissions to that account separately and scope them to the brand and task rather than inheriting full account power from a successful credential check.
- Document which flows are identity checks and which are permission checks so support and engineering do not conflate them during incidents.
Caveat: The source offers only a brief note that authorization may be layered in future, so plan your own permission model rather than waiting for the credential standard to supply one.
Caveat: A successful credential assertion proves control of the key, not the legitimacy of the underlying business request.

Tags: bot-and-agent-security, authentication, authorization, admin-accounts, integrations, account-security
Source: Site Security (1).docx

---

## Name the customer-facing credential plainly for storefront login
Use when: Writing the account-security settings copy, login buttons and help articles for your storefront.
- Pick a plain label for the physical object, since the source reports that 'security key' is roughly what everyone calls the thing in front of the user, and warns not to expose internal acronyms as English.
- Avoid relying on 'device' to mean an external token, because the source points out the same word now also means the customer's phone or laptop when they use built-in biometrics, creating confusion.
- Account for platform branding: the source observes Windows brands its biometric flow and other platforms brand theirs, so one generic button may need platform-aware labels to match what customers see on screen.
- For flows that unlock with a fingerprint or face rather than a separate key, use wording about signing in with the device or with biometrics, mirroring how the source describes the generalization.
- Test the wording against real support tickets: the source notes Android may present a chooser among key, Bluetooth, NFC, fingerprint and face, so your copy should not promise a single interaction.
Caveat: The source states explicitly that no standard naming has been settled and that naming choices confuse users; expect to iterate.
Caveat: This assumes the customer sees a platform prompt; what appears varies by browser and OS, so verify the current experience.

Tags: bot-and-agent-security, authentication, copywriting, product-page, customer-research, webauthn
Source: Site Security (1).docx

---

## Identify and Prioritize Node.js Core vs Dependency vs App Vulnerabilities
Use when: Planning a vulnerability review or patch cycle for an ecommerce storefront/backend running on Node.js, or deciding whether a scanner finding is your code, a package, or the runtime.
- Classify every finding into one of three layers: (1) Node.js core/platform, where a single bug affects every Node app on the internet; (2) the package ecosystem you depend on; (3) your own application code. Treat these as distinct in your threat model, not one bucket.
- Remember that Node core itself embeds C/C++ dependencies (OpenSSL, V8, libuv, zlib, ICU, HTTP parser and others). A vulnerability in shipped embedded code means the runtime is vulnerable — the source notes a non-trivial share of Node security releases over a two-year span were patching OpenSSL. Track core runtime patch releases, not just npm advisories.
- Because ecosystem packages become part of your application, run dependency scanning on your lockfile and map findings to the direct or transitive package that actually pulls them in.
- For each layer, decide the response: upgrade runtime version, bump/replace a package, or patch your own code. Prioritize based on reachability and your store's exposure (e.g., a DoS in a request-parsing path used on checkout is higher priority than an unused dev dependency).
- Maintain a standing process: subscribe to your runtime's security release announcements so you patch proactively rather than reacting after an exploit is public.
Caveat: The source describes open-source volunteer project process; exact announcement channels and tooling change over time — verify current Node.js security release notification methods.
Caveat: A core bug is broadly impactful but may not be reachable in your deployment; score by your own threat model rather than treating all core CVEs as automatically critical.

Tags: bot-and-agent-security, dependency-management, vulnerability-management, nodejs, patching, threat-modeling
Source: Site Security (1).docx

---

## Use CVE, CWE and CVSS as a Shared Vocabulary for Storefront Findings
Use when: Documenting or triaging a security finding in an ecommerce stack, or deciding how severely to treat a reported bug in your runtime or a package.
- Use CWE (Common Weakness Enumeration) to name the class of weakness — for example improper input validation, authentication bypass, or improper interaction between multiple correctly-behaving entities. This is a shared vocabulary for describing what went wrong.
- Use CVE (Common Vulnerability and Exposures) to look up known, disclosed findings per project. Search for your runtime or package (e.g., a CVE list for nodejs) and cross-reference version numbers against what you run in production. This lets an operations team scan what's deployed and know whether it's vulnerable.
- Score a candidate finding with the CVSS base-score calculator, working through attack vector (network vs adjacent vs local vs physical), attack complexity, privileges required, user interaction, scope, and the confidentiality/integrity/availability impacts. Network-vector, low-complexity, no-privilege, no-user-interaction findings score highest.
- Interpret the score against your own environment: the source stresses that a high CVSS score does not automatically mean high risk for your specific system — CVSS is a fairly general threat model. Combine the score with whether the vulnerable path is reachable in your store.
- Lesson for merchants: even a pure availability bug (a DoS requiring user interaction) can score in the mid-6s, so availability issues should not be dismissed as cosmetic.
Caveat: CVSS is a general-purpose scoring model, not a substitute for your own threat model; the source explicitly warns the score may overstate or understate real risk in your environment.
Caveat: CVE database entries and calculator interfaces change; verify current tools rather than assuming a fixed layout.

Tags: bot-and-agent-security, vulnerability-management, risk-scoring, cve, cvss, cwe, threat-modeling
Source: Site Security (1).docx

---

## Threat-Model Your Whole Domain, Not Just Your Software
Use when: Auditing the security of your store's external estate (DNS, subdomains, marketing pages, CDN configuration) or setting up a threat-modeling exercise for your ecommerce operation.
- Enumerate everything your store or brand exposes, not just application code: subdomains, DNS records, CNAMEs, landing pages, marketing microsites, package-registry names, and third-party service integrations.
- For each domain/DNS record, verify it still points to a service you control and activity maintains. The source describes an abandoned subdomain that pointed to a CDN provider which did not require proof of domain ownership to register a distribution under that hostname — enabling an effective takeover of the brand's subdomain.
- When you migrate or decommission a service, audit and delete stale CNAME and DNS records rather than leaving them pointing at third-party infrastructure.
- Because these domains may be the canonical source of information customers and package managers rely on, an attacker controlling one could distribute bad content or credentials before you react. Rank domain/DNS issues as genuine attack vectors, not just website trivia.
- Regularly audit your DNS estate and third-party integrations as part of a standing threat-model review, and after any infrastructure or vendor change.
Caveat: The takeover described was reported by a good-faith researcher in a specific project context; the exact CDN ownership-verification behavior may differ across providers and over time — verify each provider's current policy.
Caveat: The source presents this as one project's experience, not a benchmark of how often such takeovers occur.

Tags: bot-and-agent-security, threat-modeling, dns, domain-takeover, attack-surface, third-party-risk
Source: Site Security (1).docx

---

## Never Expose Node Inspector/Debug Ports on Storefront Servers
Use when: Running or debugging a Node.js storefront or backend on a server, or reviewing server configuration for exposed management/debug endpoints.
- Understand the risk condition: if a Node.js inspector/debug port (−−inspect, commonly port 5858) is reachable, an attacker can connect as a debugger and get full code execution. A DNS-rebinding attack demonstrated that even a malicious website open on the same machine, or another machine on the local network, could trick the browser into reaching a localhost debug port and gaining code execution.
- Do not leave the debug port open on production or on any host with network exposure. The source notes bots continuously crawl the internet looking for systems with the debug port open.
- If remote debugging is required, restrict access: bind to localhost only, use an IP address and/or SSH tunnel rather than a hostname, and lock the port down with credentials or a cookie.
- Frame this as a bounded internal validation: confirm on your own host which ports are listening, test from an external network that the debug port is not reachable, then close or gate it. Do not attempt the attack against systems you do not own.
- Track this across environments — the same risk applies to a laptop demo, a staging box, or a cloud VM, not just production.
Caveat: The DNS-rebinding technique and exact mitigation were specific to a reported Node.js CVE and affected versions; verify current Node.js documentation, since defaults and mitigations may have changed.
Caveat: Mitigation can break legitimate remote-debugging workflows; plan an alternative (IP/SSH tunnel) rather than simply reopening the port.

Tags: bot-and-agent-security, nodejs, debug-ports, dns-rebinding, remote-code-execution, server-hardening
Source: Site Security (1).docx

---

## Design an Embargo and Coordinated-Disclosure Process for Security Findings
Use when: Coordinating a fix for a known vulnerability in your store's stack, briefing contractors/vendors, or scoping who on your team can access a security finding before it is public.
- Treat reported vulnerabilities as embargoed: restrict details to those who need them to develop and test the fix. The source describes a project policy where even team members could not share embargoed vulnerabilities with colleagues at their own (or other) employers before public disclosure, and leaking could cost them their position.
- Define who is 'in scope' for embargoed information and keep the flow need-to-know. Because an early-access program for downstream runtimes was hard to implement politically and technically, employees on the security team could not pre-notify their own product teams — meaning downstream teams sometimes had breaking changes land with no warning.
- Plan the disclosure sequence: confirm and fix, cut the release, then publish the CVE, CVSS score, a blog post and an announcement. Only after public disclosure do broader teams and customers get full details.
- Where possible, use pre-announcement or advance-access channels for critical downstream partners so they can patch and test, minimizing the window between zero-day and production patching — but recognize this is difficult to run and may not be feasible for a small team.
- For your store, adopt the same discipline: brief only the engineers and vendors who must act, and set a target disclosure/patch timeline.
Caveat: The source describes an open-source volunteer project's policy and its real problems (leaks gave some vendors a competitive advantage); it is not a legal opinion and embargo rules vary by organization.
Caveat: Advance-notification programs are presented as desirable but hard to implement — do not assume they are easy or standard.

Tags: bot-and-agent-security, coordinated-disclosure, embargo, incident-response, vendor-management
Source: Site Security (1).docx

---

## Set Explicit Response SLAs for Security Reports
Use when: Running a bug-report intake for your storefront, or setting expectations with a security researcher, agency, or bug-bounty platform.
- Publish a clear acknowledgement-and-update commitment. The source project's stated SLA is to acknowledge within 24 hours and provide an update within 48 hours, tracked by a third-party platform that measures adherence.
- Use a management platform (the source uses HackerOne) to log each report, store its CVSS score and CWE, and track resolution times — the platform reports metrics such as average time to first response and to triage.
- Monitor your adherence rate to the SLA over a rolling window (the source cites meeting its standard about 92% of the time over 90 days with a team of under 20 volunteers). Treat recurring misses as a resourcing or triage-quality problem to fix.
- Where a bug-bounty platform is used, consider that it may pre-triage reports before they reach your team to filter non-issues, but pre-triage by generalists can mischaracterize platform-specific issues — so retain an internal triage step.
- Have a documented channel for reporting issues in your dependencies versus your own code, so researchers are routed correctly and your team's time is not wasted.
Caveat: Numeric SLA figures (24/48 hours, 92%) are this project's specific commitments and measured results, not universal benchmarks — set targets appropriate to your team size.
Caveat: Platform features, scoring and reputation mechanics change; verify the current interface and policy of any bug-bounty platform you use.

Tags: bot-and-agent-security, vulnerability-management, sla, triage, bug-bounty, incident-response
Source: Site Security (1).docx

---

## CSRF fundamentals: ambient cookie authority and forged state-changing requests
Use when: Auditing or designing any authenticated storefront action that changes state: add-to-cart, save address, place order, change email/password, refund, or admin config.
- Understand the mechanism: browsers automatically attach a site's cookies to requests to that site, so once a shopper logs in, any other page can trigger a request that carries their session — the source calls this 'ambient authority'.
- Identify the vulnerable surface: any endpoint that performs a state change and trusts only the cookie. Classic CSRF examples include transferring money or submitting a form the user did not intend.
- Prefer the browser-level fix first: mark session cookies SameSite so they are not attached to requests initiated by third-party sites. The source notes this is simpler and less error-prone than per-endpoint token logic.
- Keep CSRF tokens where SameSite is insufficient: the source recommends tokens especially when supporting old browsers (e.g. enterprise apps) or where framework or proxy behavior may not enforce SameSite reliably.
- Test your own store before shipping: attempt a cross-site POST to a state-changing endpoint from a separate origin and confirm it is rejected.
- Layer defense-in-depth: SameSite cookies plus tokens plus server-side checks on sensitive operations (order placement, account changes).
Caveat: SameSite alone does not cover all flows; the source explicitly says tokens remain useful for old-browser support and layered defense.
Caveat: Referer-header checks are weak: the source notes attackers can cause the Referer to be omitted, leaving servers unsure whether omission is benign or malicious.
Caveat: Do not treat a single control as a guarantee — verify behavior on your actual stack and browser support matrix.

Tags: bot-and-agent-security, checkout, csrf, session-security, cookies, authentication
Source: Site Security (1).docx

---

## Implement stateless CSRF tokens with HMAC over the session ID
Use when: Building or reviewing the anti-CSRF token layer for a storefront or admin panel, especially when you need validation across many open tabs without server-side token state.
- Issue a token to the client and require it on subsequent state-changing requests; the source describes a hidden form field (type=hidden, name like csrf_token) echoed back on submission.
- Avoid the naive approach of generating random tokens and remembering every token ever issued — the source warns that a user with many tabs breaks 'last token only' validation and forces unbounded server storage.
- Derive the token deterministically: HMAC the session ID with a secret only the server knows. The server then only needs to remember the single secret, not each token.
- Validate by recomputing the token from the session ID in the incoming request and comparing; mismatches are rejected as invalid.
- Accept that the same token is reused for the life of a session. The source says that is fine because the attacker cannot read it cross-origin and cannot feasibly brute-force a large enough token space.
- Include the token in every state-changing form (cart updates, checkout submission, account edits) so a forgotten endpoint does not silently reopen the hole.
Caveat: Security depends on the secret remaining server-only and the token space being large enough that guessing fails.
Caveat: The source notes CSRF tokens are essentially nonces; do not confuse them with CSP nonces, which restrict script execution rather than form submissions.
Caveat: A single endpoint that forgets to validate the token can expose the whole application.

Tags: bot-and-agent-security, csrf, session-security, checkout, cryptography, authentication
Source: Site Security (1).docx

---

## Why the CSRF token defeats a forged request: same-origin policy blocks token theft
Use when: Explaining, debugging or threat-modeling why a suspicious request should be rejected on an ecommerce session, and validating a token defense behaves correctly.
- Trace the legitimate flow: user logs in, server sets a session cookie and returns HTML containing the CSRF token; every later form submission includes both cookie and token.
- Trace the attack: the attacker's page submits a POST to your store; the browser attaches the victim's cookie but the attacker's JavaScript has no way to read your token value out of your page because that would violate the same-origin policy.
- Confirm the server's decision rule: even though the cookie is valid, a missing or wrong token means reject the request — the source stresses that checking only the cookie would wrongly accept it.
- Sanity-check in a test harness: verify forged cross-site posts are rejected and legitimate in-app submissions succeed, rather than trusting that the token is wired up correctly.
- Note the deeper lesson for all ecommerce integrations: a valid session is not proof that the user authorized the action — treat the token as proof the request originated from your own UI.
Caveat: The protection holds only while the token cannot be read cross-origin; XSS in your own pages defeats it entirely because injected script runs same-origin.
Caveat: The source does not claim tokens replace other controls; it presents them as the pre-SameSite solution that remains valid.

Tags: bot-and-agent-security, csrf, same-origin-policy, session-security, checkout, authentication
Source: Site Security (1).docx

---

## Validate the method, not just the token, in redirect/callback handlers
Use when: Designing or reviewing login-with-X, OAuth callbacks, payment-gateway return URLs, or any endpoint that both renders a page and performs a state change.
- Recognize the design pattern the source describes: the authorize page renders the form on GET and the form posts back to the same URL, so the handler branches on request method.
- Audit your own store for endpoints sharing one route between a safe render and a sensitive action — common in checkout return URLs, account linking, password reset links and any 'login with' flow.
- Treat the CSRF token as necessary but not sufficient: if the underlying state machine lets a request reach the action branch with a valid-but-unintended token, the token check passes while the action is still wrong.
- Require an explicit, server-tracked authorization step (e.g. an approval, a nonce bound to the user's request, or a re-auth) rather than relying solely on the form's hidden field.
- Log and alert on method anomalies (POSTs arriving from unexpected origins, repeated callbacks, unusual sequences) so you can detect bypass attempts.
- Re-test the full flow after any framework or handler refactor, since route-to-controller mapping is exactly where the source's case slipped.
Caveat: This card converts a documented bypass of a third party's OAuth flow into defensive guidance; it does not claim your store's flow is affected.
Caveat: Do not attempt these techniques against systems you do not own or have written authorization to test.

Tags: bot-and-agent-security, oauth, csrf, checkout, authentication, integration-security
Source: Site Security (1).docx

---

## Use threat modeling to choose controls, not just to list bugs
Use when: Defining the security posture for a new ecommerce platform, integration or checkout flow, or when deciding which threats warrant investment.
- Separate threat environments (server-side vs client-side code) and enumerate classes of threats with their frequency and severity for your own context.
- Make severity context-specific: the source notes severity for a threat model depends on how you run and scale — a control critical for one deployment may be minor for another.
- Include dependency and supply-chain threats, weak cryptography, unsafe deserialization or injection points, and poor developer experience as explicit categories.
- Map each threat to concrete controls (sandboxed builds, network policy, dependency pinning, install-time isolation) rather than vague 'be careful'.
- Write down which threats you are accepting and why, so the decision is visible rather than accidental.
- Review the threat model when architecture changes (new payment provider, new hosting model, new region).
Caveat: This is a general threat-modeling method, not a node-specific checklist from your environment.
Caveat: Severity ratings are context-dependent heuristics, not universal scores.

Tags: bot-and-agent-security, threat-modeling, risk-assessment, architecture, integration-security, security-process
Source: Site Security (1).docx

---

## npm install runs arbitrary code — isolate builds from production hosts
Use when: Setting up CI/CD or deployment processes for an ecommerce storefront or custom service, and deciding where dependencies get installed.
- Accept the premise: npm install may run post-install scripts, so installing is executing third-party code on that machine.
- Build inside a throwaway container or isolated build environment that is destroyed after the build, so any compromise does not persist.
- If you build on a long-lived VM instead, recognize the elevated risk: the source notes running npm install on a shared or persistent host can compromise the main system.
- Add network egress policy to the build container so it can only reach required registries/domains, cutting off exfiltration paths for compromised packages.
- Promote the built artifact, not the build host: production should receive the reviewed output, not code that was installed on a live server.
- Re-audit after any change to build tooling or the container base image.
Caveat: This is a general risk statement; it does not mean every install is malicious.
Caveat: Verification tooling and CI behavior change over time — check the current interface of your package manager and CI before relying on flags or defaults.

Tags: bot-and-agent-security, supply-chain, ci-cd, dependency-management, sandboxing, build-security
Source: Site Security (1).docx

---

## Keep a live dependency inventory and patch systemically
Use when: Running periodic dependency hygiene for an ecommerce platform or custom service, and deciding when to schedule patching.
- Run the package manager's audit command to surface known-vulnerable dependencies; the source references npm audit as an example of this class of tool.
- Compare against upstream security advisories and the project's own disclosure lists rather than relying solely on the tool.
- Track which dependency versions are running in production versus development, since only production exposure creates customer risk.
- Schedule patching as regular work, not only after a high-profile incident, so you are not perpetually behind.
- Keep installation in isolated/sandboxed environments (separate card) so installing the fixes doesn't itself introduce risk.
- Document accepted-but-unfixed issues with the reason and revisit them when the package or runtime changes.
Caveat: The source warns audit tools cannot guarantee you'll catch the next attack and warns against assuming one ecosystem is uniquely vulnerable.
Caveat: Some tools mentioned by name in the source may have changed ownership or behavior — verify the current product before adopting.

Tags: bot-and-agent-security, supply-chain, dependency-management, patching, measurement, audit
Source: Site Security (1).docx

---

## Supply-chain defense: network policy inside the build container
Use when: Hardening the build pipeline for an ecommerce storefront or service that installs third-party packages.
- Understand the attack class: the source describes a malicious package that carefully gated its payload to run only inside the victim application's dependency tree, keeping the exploit out of the GitHub source and inside the published package only.
- Accept the implication: since you may review source and still miss the payload, detect and limit by behavior and environment rather than confidence in reading code.
- Apply network policy to the build container so that even a compromised install cannot exfiltrate data or reach unexpected hosts.
- Scope the build container's filesystem access to what's needed; the source notes package installs can otherwise reach unexpected places on the host.
- Keep authentication secrets for registries and deployment out of the build environment where possible, so a compromised install cannot steal them.
- Combine with isolated builds and a dependency inventory as a layered defense rather than any single control.
Caveat: The event-stream case study is a historical example, not a current benchmark or guarantee; treat it as illustration of a pattern.
Caveat: No network policy is a complete guarantee, especially if egress rules are broad or misconfigured.

Tags: bot-and-agent-security, supply-chain, network-policy, sandboxing, ci-cd, secret-management
Source: Site Security (1).docx

---

## Never let security process strangle developer velocity
Use when: Designing or reforming the security review process for an ecommerce engineering team, especially when balancing shipping speed against compliance.
- Recognize the failure mode: if the review process is too burdensome, engineers will bypass it (create their own repos, skip reviews), and the organization ends up less secure.
- Use staged environments: let developers work freely in isolated development/sandbox environments, then run a full dependency review before anything marks production.
- Make the promotion gate specific: at review time, point out the few dependencies that cannot ship, rather than blocking the entire workflow.
- Keep the burden on the machine where possible — automation, templates, pre-checked pipelines — so the human step is quick and targeted.
- Measure friction and revisit rules that cause frequent bypasses; treat bypass as a signal, not only as a violation.
- Communicate why a rule exists so engineers can comply intelligently rather than work around it.
Caveat: This is the source's opinion about balancing security and velocity, not a universal instruction.
Caveat: Relaxed isolation still requires that production receives only reviewed artifacts.

Tags: bot-and-agent-security, security-process, ci-cd, sandboxing, developer-experience, governance
Source: Site Security (1).docx

---

## Match your threat model to the hosting/runtime model you actually use
Use when: Choosing between self-managed VMs, containers and serverless for a storefront or service, and setting cost/abuse guardrails.
- Note that in managed function runtimes the provider may patch the underlying runtime and OS image for you, so 'always update the runtime yourself' may not apply the same way.
- Recognize the changed DoS shape: with per-request isolation, a denial of service may only take down the specific instance rather than the whole service, but a resource attack can drive up metered spend.
- Set maximum scale limits and cost alarms on managed functions so anomalous traffic cannot silently drain the budget.
- Map availability concerns differently by deployment model — a DoS against a single VM looks very different from a DoS against a scaled function fleet.
- Track tenancy and scaling assumptions (one tenant per function, shared host, shared container) because they change which attacks are feasible.
- Revisit threat model whenever you migrate hosting models or scale assumptions change.
Caveat: Specific provider behaviors (e.g. which OS image or runtime is used, patching cadence) change over time and must be verified against current documentation.
Caveat: The source's example is Google Cloud Functions-era behavior and is illustrative rather than a current vendor fact.

Tags: bot-and-agent-security, serverless, threat-modeling, cost-control, availability, architecture
Source: Site Security (1).docx

---

## Stability vs. security: when not to change a component (and what it costs)
Use when: Deciding whether to swap out a core dependency, parser or subsystem in a running ecommerce platform where behavior and timing matter.
- Treat refactors that claim 'semantically equivalent' as risky in large systems: the source describes refusing even a faster parser change because changed performance characteristics could break systems that depend on timing.
- Favor no-behavior-change in maintenance branches: the source says stable/LTS branches avoid changes that could shift performance or timing, even improvements.
- When you must keep a known-imperfect component, document its risk explicitly so future maintainers know it is a conscious decision, and plan how you would respond to a future vulnerability.
- Decide in advance whether you'd patch or replace in an emergency, and flag that such a change may be communicated as a minor while being functionally breaking.
- Weigh maintenance cost: the source explains that teams may end-of-life a version early rather than carry unsupported dependencies.
- Apply the same reasoning to legacy code in a storefront: replacing a component 'just to modernize' without evaluating timing/behavior dependencies can destabilize order flows.
Caveat: This is the source's operational experience with a specific runtime, not a general rule; apply judgment to your own stack.
Caveat: Do not use this as justification to ignore known vulnerabilities indefinitely — the source frames it as an informed, documented trade-off with a response plan.

Tags: bot-and-agent-security, stability, dependency-management, risk-assessment, platform-engineering, patching
Source: Site Security (1).docx

---

## Recognize composite attacks and layered defenses
Use when: Reviewing the security posture of an ecommerce stack and deciding how to layer controls across application, runtime and infrastructure.
- Expect chaining: the source notes attackers often combine multiple known weaknesses, so an individually 'minor' bug can be a step in a serious attack.
- Treat write-out-of-bounds or memory-safety issues as potentially escalating, not merely as denial-of-service bugs, when reviewing anywhere untrusted data reaches memory-unsafe code.
- Layer controls so a failure of one (e.g. a WAF rule) does not translate directly into a breach.
- Isolate components (build containers, service instances) so an exploit's reach is contained if a layer fails.
- Keep detection breadth: since a carefully timed attack may not produce obvious errors, monitor for slow degradation, unusual resource use and timing anomalies, not just hard failures.
- Re-test defense layers after any component upgrade, since adding a new layer can create unexpected interactions.
Caveat: This is a general principle illustrated with historical examples, not a claim that your store is specifically vulnerable.
Caveat: Do not attempt to reproduce these attacks outside systems you own or are authorized to test.

Tags: bot-and-agent-security, threat-modeling, defense-in-depth, memory-safety, monitoring, architecture
Source: Site Security (1).docx

---

## Watch for slow, hard-to-detect degradation from abuse
Use when: Setting up monitoring and anomaly detection for an ecommerce backend, especially around request handling, checkout timeouts and resource exhaustion.
- Understand the pattern: the source describes requests held open slowly at a measured cadence, gradually leaking resources so the process handles requests orders of magnitude more slowly.
- Note the detection challenge: the source calls this 'really really nasty' because there may be no good way to notice that performance is degrading over time.
- Track trends, not just thresholds: monitor latency, memory and resource use over long windows so slow degradation is visible before users complain.
- Restarting clears the symptom — treat repeated unexplained slowdown followed by restart as a signal, not a routine workaround.
- Apply timeouts to slow-arriving headers or partial requests and cap the resources any single connection can consume.
- Combine with isolation so a degraded instance does not take the whole service down.
Caveat: This is a general pattern from the source; specific timeout values or mitigations may not transfer to your stack.
Caveat: Some concrete mitigation details were tied to a specific runtime version and may be outdated.

Tags: bot-and-agent-security, monitoring, availability, denial-of-service, performance, operations
Source: Site Security (1).docx

---

## Treat admin/integration endpoints as high-value attack surface
Use when: Reviewing storefront integration endpoints: login-with-provider flows, webhook receivers, admin APIs and any legacy interface still reachable.
- Map all interfaces that can authenticate or authorize action, including legacy or internal ones that may still be reachable from outside.
- When you fix a vulnerability in one interface (e.g. the new inspector/debug interface), explicitly check whether an older or parallel interface shares the same weakness — the source describes cases where the legacy path retained the same vulnerabilities after the new one was patched.
- Require authentication and authorization on every admin or integration endpoint, not just the ones on the main navigation.
- Restrict where these endpoints can be reached from (network policy, VPN, allowlists) to reduce exposure.
- Log and review access to these endpoints and alert on unexpected callers.
- Re-test after any change to authentication or routing, since changes can accidentally re-expose older paths.
Caveat: This is a general defensive principle drawn from case studies; specific interface names and version details from the source may be outdated.
Caveat: Do not attempt to exploit authentication interfaces on systems you do not own.

Tags: bot-and-agent-security, attack-surface, authentication, integration-security, admin-security, authorization
Source: Site Security (1).docx

---

## General server hardening for ecommerce stacks
Use when: Establishing baseline security hygiene for an ecommerce backend before launch or during periodic review.
- Assess your build approach: is npm install run on a persistent host or in a disposable sandbox? Prefer isolated builds (see build-isolation card).
- Inventory and audit dependencies regularly and patch them on a schedule.
- Isolate installation and execution: limit network access from where dependencies are installed so compromised packages cannot exfiltrate data.
- Recognize where your code runs determines your defenses: hosting model changes which attacks are realistic (see runtime-model card).
- Keep authentication/authorization strong end-to-end: check both cookie validity and request intent for state-changing operations.
- Remember the source's point that sandboxing supports velocity: strict auditing without sandboxing pushes teams to skip reviews.
- Document the controls in place and who owns them, so each isn't assumed without being verified.
Caveat: A checklist is not a substitute for threat modeling and testing on your specific stack.
Caveat: Tool specifics referenced in the source are historical; verify current capabilities of your package manager, CI and hosting provider.

Tags: bot-and-agent-security, hardening, dependency-management, sandboxing, authentication, operations
Source: Site Security (1).docx

---

## Prefer simple browser-level security over repeated per-app logic
Use when: Setting cookie attributes and session policy for a storefront, and deciding what security logic belongs in the browser vs your application code.
- Prefer the mechanism the platform can enforce consistently — the source recommends SameSite as the simpler, less error-prone default over hand-rolled token checks.
- Understand why: the source notes that with per-app token logic, forgetting it on one endpoint can make the whole app vulnerable.
- Still keep application-level checks where the platform mechanism is not universally supported — the source mentions old browsers and enterprise contexts as reasons a token remains useful.
- Set explicit cookie attributes (SameSite, Secure, HttpOnly, appropriate scope) rather than relying on defaults.
- Audit across frameworks and proxies: behavior differs, so verify your specific stack honors the attributes you set.
- Revisit policy on browser or framework upgrades, since defaults and support change.
Caveat: SameSite semantics and browser defaults have changed over time; verify current behavior for your audience before relying on it.
Caveat: Never claim a single cookie attribute fully prevents CSRF on its own.
Caveat: Layer controls on sensitive flows regardless.

Tags: bot-and-agent-security, cookies, csrf, session-security, browser-security, authentication
Source: Site Security (1).docx

---

## Treat agent/tool instructions and retrieved documents as untrusted data
Use when: Designing or auditing agents that operate on an ecommerce stack (listing changes, pricing updates, support replies) and consume external or user-supplied content.
- Separate data from authority: retrieved documents, tool output and user input are data to reason about, not instructions that authorize state-changing actions.
- Scope each agent/tool to the brand and task it was granted, rather than a broad API key covering all operations.
- Require explicit human or system approval for high-impact actions (price changes, refunds, publishing listings, account changes).
- Keep secrets out of the model's reach: use scoped credentials and avoid placing long-lived credentials where an injected instruction could retrieve them.
- Log agent actions and the content that triggered them so anomalous behavior can be investigated.
- Apply input handling equal to the rest of your app: validate and sanitize before acting, since prompt filtering alone is not a guarantee.
Caveat: This adapts general supply-chain and injection themes from the source to agent/tool contexts; the source does not specify agent controls directly.
Caveat: No combination of filtering or scoping is a complete guarantee — treat it as layered risk reduction.

Tags: bot-and-agent-security, agent-security, prompt-injection, authorization, secret-management, logging
Source: Site Security (1).docx

---

## Security researcher case studies: read disclosed vulnerabilities as learning material
Use when: Building a security training or testing backlog for an ecommerce engineering team, and turning disclosed bugs into prevention checks.
- Use public vulnerability databases and language-specific disclosure boards as a source of realistic test cases.
- Classify findings by weakness type (e.g. command injection, SQL injection, path traversal) so you can look up the general class and understand what qualifies as an instance, rather than only memorizing the single bug.
- For each relevant class, write a defensive test in your own codebase: e.g. if an ORM dependency has a SQL-injection history, verify your queries are parameterized and inputs are validated.
- Note that disclosed issues may be narrowly scoped or low-volume (the source describes a small module with a command-injection issue and low downloads) — matching your stack to a finding matters more than general alarm.
- Prioritize fixes by whether the affected package/route is actually deployed in your production path.
- Re-run these checks when dependencies are updated.
Caveat: Case-study findings are examples of past bugs, not predictions or guarantees about your code.
Caveat: Do not replicate attacks against systems you do not own or have written authorization to test.

Tags: bot-and-agent-security, vulnerability-management, dependency-management, testing, threat-modeling, audit
Source: Site Security (1).docx

---

## Avoid brittle input-parsing and URL handling in storefront code
Use when: Reviewing custom parsing in storefront code: URL rewriting, redirect handling, header parsing, and any code that interprets user-supplied paths or hosts.
- Prefer well-maintained parsers/libraries over custom string manipulation for URLs, headers and structured input.
- Treat mismatches between encodings (the source references specific encoding edge cases) as potential out-of-bounds or misinterpretation risks and validate input at boundaries.
- For redirect and URL handling, restrict to allowed destinations rather than trusting user-supplied hosts.
- Be wary of combining user-controlled header sizes or timing — the source describes crafted header patterns causing failures, so cap sizes and timeouts.
- For request splitting or smuggling risks, ensure consistent parsing between proxies/load balancers and your application server.
- Keep runtime and dependencies patched, since many of these are fixed upstream.
Caveat: Specific CVE identifiers and encoder names referenced by the source are historical and may not be current; verify against your runtime's advisory feed.
Caveat: This is a general hardening principle, not a claim that your store is affected by these specific bugs.

Tags: bot-and-agent-security, input-validation, url-handling, parsing, patching, application-security
Source: Site Security (1).docx

---

## Assign threat owners and triage routes before an incident
Use when: Setting up vulnerability intake and disclosure handling for an ecommerce platform team or a vendor it depends on.
- Define who owns triage for each surface: core platform, third-party dependency, integration or hosting provider.
- Set up a channel for researchers and users to report issues, and document expected response paths.
- Expect false positives — the source notes misrouted reports — so the triage process should check scope before escalating.
- Track vulnerabilities found by internal staff or steering groups, not only external reports, so findings are not lost.
- Decide against a stated policy how you will respond when a vulnerable component cannot be patched immediately (see the stability vs security card).
- Review the process periodically and after any significant incident.
Caveat: The source describes a specific project's triage structure; your organization's intake will differ.
Caveat: This does not establish any specific SLA or benchmark.

Tags: bot-and-agent-security, vulnerability-management, incident-response, security-process, governance, triage
Source: Site Security (1).docx

---

## Method-specific routes prevent CSRF bypass via HEAD
Use when: Designing or reviewing storefront routes that handle form submissions, cart mutations, checkout actions, or any endpoint that changes account or order state.
- Register one handler per HTTP method instead of one function that branches on GET vs POST. A get/post combined controller leaves room for a third method (HEAD) to land in unintended code.
- If you must share a URL, use explicit `else if request.post` style branching rather than a bare `else`, so only the intended method runs the sensitive path.
- Add a final `else` that throws and aborts on any unrecognized method. Assume unknown methods can reach this code.
- Know that CSRF middleware is typically configured to validate only POST. A HEAD arriving at the same handler skips that check because it is not a POST.
- Validate the CSRF token explicitly, in the same block that grants a sensitive permission (e.g., authorizing an app, changing an order), not only in framework-level middleware.
- Prefer framework-level protections that bind the session by origin (e.g., SameSite cookies in lax mode) so the form-submission path doesn't rely on a manual token at all.
- Verify the current behavior of your framework (Rails, Express, etc.) before relying on it — routing and middleware auto-handling has changed over time.
Caveat: SameSite strict mode can break legitimate top-level OAuth/login redirects; lax mode permits top-level navigation cookies while still blocking cross-site subrequests.
Caveat: Framework-provided CSRF handling is a convenience, not a guarantee — do not assume it covers every method or URL.

Tags: bot-and-agent-security, checkout, csrf, authentication, server-hardening, http-methods
Source: Site Security (1).docx

---

## Fail fast when an assumption is violated
Use when: Writing or reviewing server handlers for cart operations, order state transitions, or any multi-step process where a mid-step exception would leave inconsistent state.
- Distinguish expected failures from unexpected ones. A user-supplied ID not found in the database is expected — return a 404 and keep the server running.
- An exception you did not anticipate means you no longer know the program's state (partial writes, held resources, half-completed transactions). Do not log-and-continue.
- On unanticipated exceptions, abort or throw so the process surfaces the problem. Have a supervisor restart the process.
- Set up alerting on uncaught exceptions so a violated assumption (e.g., an unexpected HTTP method reaching a handler) triggers immediate investigation.
- Add explicit assertions verifying assumptions about inputs up front, so a wrong state fails at the boundary rather than deep in logic.
Caveat: Source frames these as taste and trade-offs, not hard rules.
Caveat: Crashing on an unhandled case can be exploited for availability attacks (one request crashes an instance); weigh this against the far worse outcome of silently authorizing the wrong action.

Tags: bot-and-agent-security, server-hardening, error-handling, observability, checkout
Source: Site Security (1).docx

---

## Fixleakyabstractions that hide security-relevant detail
Use when: Choosing or building an ecommerce framework layer, integration SDK, or internal API that other code on your store depends on.
- Audit abstractions where the framework auto-handles a case for you (e.g., auto-routing HEAD to a GET handler then stripping the body). Ask what else can arrive on that code path.
- When an abstraction exposes a behavior the developer must remember in edge cases, either remove the special case or make it explicit and documented.
- Count interactions, not components. Adding one new feature that can touch 500 existing parts of the system is far riskier than an isolated addition — pay the complexity cost where it buys the most.
- Favor explicit, verbose code over clever one-liners in security-sensitive paths; clever code that even its author can't re-read a month later hides bugs.
- When reviewing, treat duplicate-looking checks (e.g., a token validated twice) as acceptable defensiveness rather than redundancy to trim — the unused-argument that controls behavior is often load-bearing.
Caveat: Source concedes this is a trade-off: requiring developers to be explicit risks them forgetting; favoring magic risks it biting you.
Caveat: Security through obscurity (hoping code is too clever to understand) is not a defense.

Tags: bot-and-agent-security, server-hardening, code-review, frameworks, complexity
Source: Site Security (1).docx

---

## Avoid APIs with insecure defaults or polymorphic signatures
Use when: Selecting a library or designing an internal helper (e.g., a data-encoding, password, or serialization utility) for your store's backend.
- Prefer APIs whose secure mode is the default. If the only safe usage requires passing a specific options object, most callers will miss it and run insecurely.
- Watch for polymorphic signatures: one function that behaves differently by argument type (jQuery's `$()` is the classic case) or by the count of callback arguments (Express middleware vs error-handling middleware differing by a 4th argument).
- Avoid relying on 'arity' tricks in your own code; make the mode explicit so a teammate can't 'clean up' an unused argument and silently change behavior.
- When evaluating a dependency, request a concrete example of how it is called in its most common path, then check whether that path validates input and fails closed.
- Check numerical/array/string coercion carefully. Coercing a user-supplied string to bytes or memory is where type confusion becomes a memory-disclosure bug.
Caveat: Source's conclusions apply to libraries generally; verify current library behavior and options before adopting, since APIs change.
Caveat: Explicit options add friction and can be forgotten, so pair explicit design with tests that assert the secure path is active.

Tags: bot-and-agent-security, server-hardening, api-design, dependencies, code-review
Source: Site Security (1).docx

---

## Uninitialized-buffer disclosure: prevent leaking memory from user input
Use when: Reviewing any backend endpoint that turns user input into bytes, encodings, or binary data — e.g., image/thumbnail generation, PDF export, or a convert/encode utility in your store.
- Require the user-supplied field to be the expected type before conversion. If you expect a string, validate `typeof === 'string'` (or original JSON type) and reject numbers, arrays, or objects.
- Do not pass user input directly into a buffer/allocation call. A string is converted to its bytes; a number is interpreted as a length and returns that many bytes.
- Ensure any buffer/allocator you use zero-fills memory or is initialized before use. Uninitialized allocation can return previously-freed process memory, which may contain earlier requests, tokens, or user data.
- Apply this to any 'nice-to-have' convert/encode helper: a convenience endpoint on an ecommerce backend can expose randomness from memory you never meant to send.
- If you cannot guarantee zero-fill, constrain the operation so an attacker cannot control a byte length or trigger repeated reads.
Caveat: This is a vulnerability condition and prevention, not a payload recipe — test only on systems you own or are authorized to test.
Caveat: The source's demo shows the exposure can include source code and prior process memory; do not treat size limits alone as sufficient.
Caveat: This class of bug parallels Heartbleed-style over-reads; apply the same principle: never return bytes you didn't intend to send.

Tags: bot-and-agent-security, server-hardening, data-exposure, input-validation, memory-safety
Source: Site Security (1).docx

---

## Bind listeners to the intended interface
Use when: Deploying or testing a store's backend, admin panel, or internal tool — especially during development before it goes behind a load balancer.
- When starting a listen call, pass the intended interface (e.g., localhost) rather than omitting the host argument.
- Verify what your framework/process manager defaults to, since 'port only' often means 'every interface on this machine'.
- For anything exposed beyond your machine, put authentication and TLS in front rather than relying on the network boundary.
- During local development, keep dev servers bound to localhost so neighboring machines on the same network can't reach them.
- Confirm behavior against the current documentation, as defaults and interfaces differ by runtime.
Caveat: Source frames the open-listener default as an example of an unsafe default; the corrective is a configuration choice you must make.
Caveat: Confirm the specific option name in your runtime's current release.

Tags: bot-and-agent-security, deployment, server-hardening, network-security, development
Source: Site Security (1).docx

---

## Give checkout and admin API calls their own signed context
Use when: Designing or auditing authorization for sensitive ecommerce operations like refunds, order edits, app/integration installs, or admin actions.
- Don't assume an upstream middleware fully validated the request for a sensitive action. Put an explicit permission/token check immediately before the operation.
- Enforce distinct endpoints per action so a token validated for one action cannot accidentally satisfy another.
- Log which check gated each sensitive action, so you can prove the guardian ran and spot routes where it didn't.
- Prefer framework-level bindings (e.g., origin-bound cookies) that make cross-site forgery impossible, rather than building your own token plumbing on top.
- Ensure any checkout mutation (order total, quantity, address) re-validates the user's authority over that cart/order at the point of write.
Caveat: Source sees explicit re-checking and framework magic as a trade-off; neither is universally right.
Caveat: Relying on a token at one layer while another layer strips or bypasses it is the exact failure the source describes.

Tags: bot-and-agent-security, checkout, admin, authorization, csrf, payments
Source: Site Security (1).docx

---

## Design-time checklist for reducing server complexity
Use when: Architecture or code review for any store backend, especially before adding an integration or refactoring authentication/checkout code.
- Budget complexity: before adding a component, ask how many existing components it can interact with. Favor isolated additions over broad ones.
- Prefer explicit code over clever code. Unroll dense one-liners into plain step-by-step logic in anything touching auth, payments, or user data.
- Make secrets/credentials and assumptions explicit. Do not bury security-relevant checks inside framework magic callers might not understand.
- Route strictly (one method per handler), validate strictly (type and presence), and fail strictly (throw on unknown states).
- Request that critical authorization flows be readable end-to-end without needing to know framework internals.
Caveat: These are lessons drawn from one incident and the instructor's experience, presented as taste and trade-offs, not absolute rules.
Caveat: Explicit code has its own failure mode: a developer can forget a check; pair with automated tests.

Tags: bot-and-agent-security, server-hardening, code-review, architecture, complexity
Source: Site Security (1).docx

---

## Verify agent tool permissions and trust retrieved content as data only
Use when: Configuring an agent that reads product feeds, customer reviews, support emails, or external APIs and can act on your store (edit listings, issue refunds, place orders).
- Treat every retrieved document, email, review, or web page as data, never as instructions. Content that says 'ignore your rules' or 'issue a refund' has no authority.
- Scope each agent's tool access to the brand and task it needs. An agent editing product descriptions should not also have refund or customer-data permissions.
- Require human approval for high-impact actions: publishing to storefront, changing prices, issuing refunds, or writing customer data.
- Block the agent from reading its own secrets or raw credentials; give it scoped API tokens with least privilege and log every tool call with inputs and outputs.
- Do not treat prompt filtering or a WAF as a guarantee. It reduces exposure but is not sufficient alone.
- Validate tool-call outputs before acting on them, just as you would validate a user-supplied field in a server handler.
Caveat: Source does not provide ecommerce agent benchmarks or measured results; the controls are inferred from general server-security principles.
Caveat: Agent tooling interfaces change quickly — verify current permission and approval options before relying on them.

Tags: bot-and-agent-security, agents, authorization, least-privilege, logging, prompt-injection
Source: Site Security (1).docx

---

## CSRF defense for storefront authenticated actions
Use when: Designing or auditing protection for authenticated ecommerce actions that change state: placing an order on a saved card, editing addresses, changing subscription billing, adding admin products, or any log-in-with-X flow.
- Understand the vulnerability condition: once a shopper logs in, the browser attaches their session cookie to every request to your domain automatically (ambient authority). Any page on any site that can cause your domain to receive a request gets that cookie attached for free.
- So an attacker page can fire a request at your store's sensitive endpoint (e.g., change shipping address, redeem stored value, approve an OAuth grant) and your server, seeing a valid cookie, treats it as the logged-in shopper.
- Prefer SameSite cookies as the primary control: set the session cookie SameSite=Lax or Strict plus Secure and HttpOnly, so cookies are not attached to cross-site requests. Lax still allows top-level navigations (needed for OAuth redirects and login), Strict is more restrictive.
- If you must support very old browsers or legacy code, layer a synchronizer CSRF token: server issues a secret nonce embedded in the page as a hidden field; the client must echo it on submissions and the server rejects requests missing or mismatching it.
- Make tokens stateless and scalable: derive the expected token by HMAC-ing the session ID with a server-only secret, so you do not have to store every token you ever issued (the source notes users can hold many tabs, so storing only the last token fails).
- Apply the control on every state-changing endpoint, not just checkout. The source's caution is that forgetting one endpoint leaves the whole app exposed.
Caveat: SameSite tokens and CSRF tokens are both effective; the source calls SameSite simpler and less error-prone, and CSRF tokens largely legacy but still common in real codebases.
Caveat: CSRF tokens still appear in frameworks such as Ruby on Rails and via Express packages like csurf; when inspecting or inheriting code, expect them and verify current framework defaults.
Caveat: HMAC-based stateless tokens reuse one token per session, which the source accepts because the token is unguessable and never shared.

Tags: bot-and-agent-security, checkout, account-security, csrf, cookies, authentication, web-framework
Source: Site Security (1).docx

---

## CSRF token bypass via HTTP HEAD and framework magic
Use when: Reviewing route handlers, OAuth/SSO callbacks, or any endpoint that mixes HTTP methods, especially where an external integration can be auto-approved for a shopper or merchant account.
- Vulnerability condition: a single controller/handler serves both GET (render a consent page with a CSRF token) and POST (validate token, then grant access), branching on the request method.
- A common framework (Ruby on Rails; Express also does this for HEAD) routes HEAD requests to the GET handler automatically and strips the response body, because HEAD is semantically like GET and assumed side-effect-free.
- But in the handler, the developer's method check (e.g., request.get?) returns false for HEAD, so control falls into the else branch intended for POST. Meanwhile the framework's POST-only CSRF pre-check never runs for HEAD.
- Result: a HEAD request to the authorize endpoint, with the victim's cookies attached, granting an attacker-controlled app access without any CSRF token and without user interaction. Exercised in the source's case by merely visiting a page.
- Prevent it by not merging methods: use separate routes/handlers for GET (render) and POST (mutate), or branch with explicit else-if on the POST method and an else that throws, so an unexpected method aborts rather than falling through into sensitive logic.
- Prefer validation attached directly to the sensitive grant (the source presenter favors explicit, less 'magical' checks over relying on framework-level POST-only CSRF middleware) rather than assuming an upstream layer already validated.
Caveat: The GitHub case study is a historical, now-fixed incident (reported via HackerOne, acknowledged in minutes, fixed in hours per the source); it is an example, not a current claim about GitHub.
Caveat: Framework routing behavior for HEAD is version- and framework-dependent; verify the current behavior of your own framework rather than assuming.
Caveat: Forcing a CSRF token onto HEAD requests is possible but changes HEAD semantics for legitimate public resources, so it is not a clean universal fix.

Tags: bot-and-agent-security, oauth, authentication, api-security, web-framework, routing, integration-security
Source: Site Security (1).docx

---

## Defensively whitelist HTTP methods in store endpoints
Use when: Writing or reviewing route handlers for cart, checkout, subscription, account, or admin endpoints where method confusion could trigger an action a shopper did not intend.
- When a handler branches on method, never write a two-way if/else that assumes only the two methods you expect. Write if (GET) {...} else if (POST) {...} else { throw/abort }.
- Rationale from the source: a crash on an unexpected method is far better than silently running sensitive code. Crashes surface as production exceptions and alerts, letting you discover and fix the violated assumption quickly.
- Mechanism preference: in frameworks like Express, register per-method routes (app.get, app.post) rather than a catch-all (app.use) that receives every method and forces you to handle them all.
- Ordering advice from the source: do not rely on upstream framework middleware to enforce a security check for a sensitive action; place the relevant validation explicitly on the sensitive path so a new developer or a new route cannot silently skip it.
- Reject the source's leaky-abstraction trap: if your framework auto-routes one method to another's handler (HEAD to GET), make sure your internal method checks still match reality, or avoid framework-level assumptions entirely.
Caveat: The source presents this as a trade-off: explicit checks are less magical but easier for a developer to forget in one place; framework magic is convenient but can hide the exact failure that occurred here.
Caveat: An attacker who discovers a crash path can affect availability (crash one or many instances), which the source accepts as the lesser evil versus an authorization bypass.

Tags: bot-and-agent-security, checkout, api-security, routing, input-validation, web-framework
Source: Site Security (1).docx

---

## SameSite strict vs lax: don't break OAuth login on your storefront
Use when: Configuring session cookie attributes for a store that uses 'Log in with Google/Twitter/X' or any third-party identity provider redirecting back into checkout.
- Understand the trade-off: Strict never attaches the cookie on cross-site requests, which maximizes CSRF safety but blocks legitimate flows where the browser is navigated from an external site (or app) into your domain.
- Lax permits the cookie on top-level navigations (the whole browser going to GitHub/Google/your domain) while still blocking most cross-site sub-requests, so OAuth-style login redirects keep working.
- For OAuth specifically, the provider typically forces a top-level page where the user clicks Authorize; the source notes providers use this interactive step partly because the session cookie would not otherwise be sent. Plan your flow around a real user click, not a silent request.
- If your store uses OAuth for merchant or admin apps (app-store-style integrations), test the full redirect chain with your chosen mode before rollout: verify the callback receives cookies and the token exchange succeeds.
- Do not set Strict as a blanket default on cookies that must traverse cross-site navigation chains; verify each cookie's required behavior individually.
Caveat: SameSite modes and browser default treatment have changed over time; verify current browser and framework defaults rather than assuming historical behavior.
Caveat: This is a design trade-off, not a universal rule: pick Strict or Lax per cookie based on which cross-site navigations that cookie must survive.

Tags: bot-and-agent-security, authentication, oauth, cookies, checkout, account-security
Source: Site Security (1).docx

---

## Leaky abstractions in frameworks cause security bugs
Use when: Evaluating framework conveniences when building storefront features, especially anything the framework implements 'for you' that touches method dispatch, auth, or CSRF.
- Identify leaky abstractions: conveniences that mostly work but expose an edge case the developer never sees. The source's example is Ruby on Rails (and Express) routing HEAD to the GET handler and stripping the body.
- For each framework convenience in your stack, ask what states or methods can reach your code that you did not explicitly account for.
- Mitigate by not building sensitive logic on top of assumptions the framework conceals: use explicit method branches, separate routes, or direct validation rather than trusting an upstream layer to have handled a case.
- The source's fix options, in its words, include: have the framework lie and report HEAD as GET so the abstraction is not leaky; or stop auto-handling and force developers to handle HEAD explicitly (losing the convenience).
- Present this as a genuine trade-off: explicit less-magical code reduces hidden failure modes but is easier to forget in one place; magical code is convenient but can bite exactly as it did here.
Caveat: This is the presenter's framing and opinion on a trade-off, not a universal rule; weigh convenience against exposure for each feature.
Caveat: Framework behavior differs by version and framework; validate against your actual stack configuration.

Tags: bot-and-agent-security, web-framework, routing, api-security, risk-management
Source: Site Security (1).docx

---

## Defensive coding: assert assumptions and fail closed on sensitive actions
Use when: Implementing any endpoint that grants access or changes something valuable: linking a payment provider, adding an admin integration, approving an app, or changing payout/bank details on a merchant account.
- For a sensitive action, do not assume an upstream layer validated it. Place the validation directly before the grant, so any new code path or developer cannot silently skip it.
- Example from the source: an OAuth authorize endpoint granted app access inside the else branch, assuming Rails had already validated the CSRF token for POSTs. A HEAD request reached that branch without the check ever running.
- Replace 'else' with 'else if method matches' plus an 'else { throw }', so unexpected methods abort catastrophically instead of falling through into the grant.
- For high-value flows, prefer explicit checks tied to the sensitive operation over reliance on framework-wide middleware, even though middleware is less repetitive.
- On abort, fail closed: throw, log, and alert so the violated assumption surfaces immediately, then fix the root cause rather than attempting recovery.
Caveat: The source frames this as a trade-off between explicitness and framework convenience, not an absolute rule.
Caveat: A deliberate crash means an attacker can cause availability impact; the source accepts this as preferable to a silent authorization bypass.

Tags: bot-and-agent-security, authentication, api-security, integration-security, risk-management, logging
Source: Site Security (1).docx

---

## Split storefront routes by HTTP method and purpose
Use when: Designing URL and route structure for storefront consent pages, integration authorization, subscription management, or any page that both renders a form and processes its submission.
- Avoid a single route/controller that both renders a page and mutates state based on method. The source identifies this merged handling as the enabling condition of the GitHub bypass.
- Instead, split into two routes or two handlers: one GET that renders the consent form (with a token), one POST that validates and mutates. The source notes the URLs could still be the same if the framework allows separate controllers per method.
- Benefit: the POST handler carries its validation directly, and unexpected methods cannot fall from a GET path into mutation logic via a shared else branch.
- Apply this pattern to storefront operations like saving a payment method, approving an installed app, or changing subscription terms, where one URL currently does double duty.
- Separate URLs are one of the recommended fixes the source lists, alongside explicit method branching and enforcing the validation on the grant itself.
Caveat: Using the same URL with separate per-method controllers is also acceptable; the key is that method-specific logic and its security check are not conflated in one branch.
Caveat: This is a design recommendation from the source, not a framework requirement.

Tags: bot-and-agent-security, routing, api-security, checkout, integration-security, web-framework
Source: Site Security (1).docx

---

## Governing agent and integration access with OAuth scopes
Use when: Authorizing third-party apps, marketing tools, or agents to act on a store (read orders, edit products, access customer data), or onboarding any OAuth-based integration into checkout/admin.
- Recognize what the grant is: after a user clicks Authorize, the provider returns a token the app uses out-of-band to access that account's data; the source describes this token as effectively the password to the account for that app.
- For store integrations, treat granted scopes as standing permission: an app with broad scope can read private data and take actions even when the user is absent.
- Minimize scope at authorization time and prefer tokens that expire or can be revoked, since a leaked or over-scoped token gives broad account access.
- Review the consent flow for silent vs explicit approval: the source's vulnerability let an attacker-controlled app be granted with no user interaction and no CSRF token. Verify your own integration flow cannot be auto-approved by a crafted request.
- Keep the human consent step genuinely interactive (the source notes providers rely on a real top-level page and click), and validate the approval endpoint defensively as in the related method-bypass card.
Caveat: The GitHub vulnerability specifics are historical and fixed (per the source: acknowledged quickly via HackerOne, fix out in hours); do not treat them as current behavior of any provider.
Caveat: OAuth scope names, token lifetimes, and consent UX are provider-specific and change over time; verify against the current provider documentation.

Tags: bot-and-agent-security, oauth, integration-security, authentication, permissions, account-security
Source: Site Security (1).docx

---

## Responding to reported vulnerabilities on your store
Use when: Setting up or triaging a vulnerability reporting process for a store, theme, app, or integration, especially for sites running your code or processing shopper data.
- Establish a low-friction report channel (the source references a bug bounty program and third-party disclosure platforms like HackerOne), and scope it to systems you actually own and are willing to reward for.
- Expect reports to include high-impact issues like cross-site scripting that can change scores or leak data; the source recounts XSS findings that could alter assignment scores and a design flaw that exposed hidden test cases, showing even 'internal' pages matter.
- Triage by impact and act fast on severe, easily reproduced issues: the source notes GitHub acknowledged a critical OAuth bypass almost immediately and shipped a fix within hours because severity was high and reproduction was trivial.
- Reproduce and confirm before paying or closing; the source notes some findings received no reward because the affected site was outside the bounty scope, so publish explicit scope to avoid disputes.
- Feed confirmed findings back into defensive coding practices (method whitelisting, validation on sensitive paths) rather than patching only the one symptom.
Caveat: The source's case study timings (minutes to acknowledge, hours to fix) are a specific example, not a benchmark or promise.
Caveat: Bug bounty coverage and reward amounts are program-specific; students in the source got $100 for one XSS and nothing for out-of-scope findings.

Tags: bot-and-agent-security, vulnerability-management, incident-response, customer-data, risk-management
Source: Site Security (1).docx

---

## Treat Leaky Abstractions as Likely Edge-Case Holes in Store Code
Use when: Reviewing or building shared ecommerce code (library, middleware, internal SDK) that wraps HTTP requests between storefront, checkout, fulfillment or third-party integrations.
- Map every case the abstraction claims to handle versus every case the underlying layer can actually deliver. The source's example: the abstraction was written for GET and POST, but HEAD requests still reached the developer's code, which had no case for them and was never told to write one.
- Before releasing a wrapper, enumerate all possible inputs (HTTP methods, parameter types, content types) and confirm each has an explicit branch or an explicit rejection — not an implicit fall-through.
- Treat any abstraction with many edge cases as 'leaky' and prefer exposing the essential cases explicitly rather than one clever catch-all that mostly works.
- If you cannot avoid a leaky wrapper (e.g., a framework's middleware signature), document the hidden requirement loudly in the wrapper so callers don't silently drop it.
Caveat: The source presents this as experience-based taste, not a hard rule; everything here is framed as a trade-off, so apply judgment to each wrapper rather than banning abstraction outright.
Caveat: The $25K loss mentioned is an illustrative anecdote, not a benchmark you can rely on.

Tags: bot-and-agent-security, code-review, integrations, maintainability, defensive-coding, checkout
Source: Site Security (1).docx

---

## Reduce Component Interactions, Not Just Component Count
Use when: Scoping a new storefront integration, payment provider connection, fulfillment hook, or automation connector before adding it to the ecommerce stack.
- For each proposed addition, ask 'how many existing components can this interact with?' rather than 'how many components am I adding?'
- If a new store component or third-party integration could reach 500 other services (e.g., a generic webhook or admin API key with broad scope), treat the change as high-risk and isolate it.
- Design the addition so it talks to as few things as possible — e.g., scope a fulfillment or inventory integration to only the endpoints it needs, so a compromise has a limited blast radius.
- Count interaction paths, not surface area: 1 component touching 1 is far less scary than 1 touching everything.
Caveat: The '500 components' figure is the source's illustrative example, not a measured threshold.

Tags: bot-and-agent-security, architecture, integrations, least-privilege, fulfillment
Source: Site Security (1).docx

---

## Use Explicit Code Over Clever Code in Security-Relevant Paths
Use when: Writing or reviewing checkout, auth, payment or PII-handling code where future maintainers must be able to verify behavior.
- Unroll clever one-liners into plain sequential steps (do this, then this, then this) so the flow is auditable, even if it looks uglier.
- Prefer obvious control flow over packed functionality; the source notes that writing less clever code tends to happen as engineers are bitten by clever code they can't re-read a month later.
- Treat 'hard to understand' as a defect in any code path that touches money, credentials or user data, because obscurity is not security.
- Do not rely on making code hard to read as a defense — the source explicitly rejects security through obscurity.
Caveat: The source treats this as career-acquired taste and a trade-off, not a universal coding mandate.

Tags: bot-and-agent-security, code-review, checkout, defensive-coding, maintainability
Source: Site Security (1).docx

---

## Fail Early on Unexpected State; Handle Expected Errors Gracefully
Use when: Deciding how a store's server should behave when errors occur — e.g., product lookups, cart operations, payment callbacks.
- Distinguish expected from unexpected errors. Example from the source: a user-typed URL for a nonexistent user ID is an expected failure — return a 404 and keep the server running.
- For unexpected exceptions (e.g., an uncaught exception in the middle of a multi-step process), do not just log and continue; the source argues you can't know what state you left behind and what cleanup was skipped.
- Let the process crash and be restarted by a supervisor, and run multiple instances so crashes don't cause user-visible downtime.
- Verify your server actually restarts on crash (process manager or orchestrator) before relying on this pattern.
Caveat: The source explicitly refines its own earlier advice: crashing is for unexpected errors, not for expected, handled ones like a missing resource.

Tags: bot-and-agent-security, error-handling, availability, checkout, defensive-coding
Source: Site Security (1).docx

---

## Assume Inputs Are Wrong: Verify Assumptions at the Top of Each Function
Use when: Building any store endpoint or handler — product search, discount application, admin actions — that trusts request parameters.
- Do not assume a function is called with the correct arguments; validate the arguments and the request payload at the start of the handler.
- Validate type and shape explicitly. In the source demo, the handler checked that a required field existed and that a type field was one of a small allowed set before proceeding.
- After validation, the rest of the handler can proceed on the assumption that inputs are in the expected state (fail fast, then continue confidently).
- For security-relevant values (IDs, amounts, resource names), verify the assumption rather than trusting caller-provided types.
Caveat: Defensive validation reduces but does not remove risk; the source presents it as one of several trade-off-based lessons, not a guarantee.

Tags: bot-and-agent-security, input-validation, defensive-coding, checkout, api-design
Source: Site Security (1).docx

---

## Reject APIs Whose Insecure Path Is the Easy Path
Use when: Choosing or wrapping third-party libraries and SDKs for a store — payment processors, auth providers, encryption helpers, bot-defense tools.
- Check the defaults: does calling the function with no options produce secure, sensible behavior? If not, treat it as a footgun.
- If you must use it, wrap it in your own function whose defaults are secure, so store developers can't accidentally invoke the unsafe path.
- Also flag polymorphic signatures — functions that do different things based on argument type or count — as harder to use correctly, especially in loosely typed languages, and prefer explicit alternatives where available.
Caveat: The source presents this as an opinion about good design, not a universal rule; some widely used libraries (jQuery, Node buffers, Express middleware) violate it, so any workaround must be tested against the specific version.

Tags: bot-and-agent-security, api-design, integrations, secure-defaults, dependency-review
Source: Site Security (1).docx

---

## Watch for Hidden Behavioral Switches in Function Signatures
Use when: Reviewing or refactoring middleware, hooks or plugin functions in a store's web framework where behavior depends on signature shape.
- Treat argument count as part of the contract in frameworks that use it. The source's example: an Express middleware becomes error-handling middleware specifically when it takes four arguments, including an otherwise-unused error parameter.
- Do not delete 'unused' parameters during cleanup — removing them can silently change a handler from error-handling to a normal middleware, breaking error flow.
- When adding middleware (e.g., CSRF token validation on POST), confirm exactly how the framework routes requests through it and which signature triggers which path.
- Verify behavior against the framework's current documentation, since this interface can change between versions.
Caveat: Express's behavior is described as of the source's version; verify the current interface before relying on the exact argument-count rule.

Tags: bot-and-agent-security, api-design, web-framework, csrf, code-review
Source: Site Security (1).docx

---

## Secure Binary/Buffer Encoding Endpoints Against Memory Disclosure
Use when: Building or auditing any store endpoint that handles binary data, encoding/conversion, or user-supplied buffer-like inputs.
- Do not build buffers from unvalidated user input where a number could be mistaken for a size. The source demo: passing a JSON number instead of a string caused the process to allocate memory that was never zeroed, and the response contained leftover process memory, potentially including credentials.
- Validate the type and length of encoding inputs explicitly (e.g., allow only string data of bounded length for hex/base64 conversion) and reject unexpected types.
- Prefer current, non-deprecated buffer/typed-array APIs and verify their initialization behavior against current documentation; when in doubt, zero or explicitly fill the buffer.
- Treat this class of bug as a memory-disclosure risk — the source notes it resembles Heartbleed-style leaks, where repeated requests can eventually expose a server's TLS key.
Caveat: The source's demo used a then-current Node Buffer constructor; the specific API may be deprecated now, so confirm against the current runtime.
Caveat: Everything here must be validated only on systems you own and are authorized to test.

Tags: bot-and-agent-security, memory-safety, input-validation, api-design, testing
Source: Site Security (1).docx

---

## Never Bind Servers to All Interfaces by Default
Use when: Deploying or configuring any store service — API, admin panel, internal tool — where bind address and exposure matter.
- Check every server start: if you omit an address/host argument, the service may listen on all interfaces, meaning anyone who can reach the host's IP can connect.
- For local-only or private services, bind explicitly to localhost/loopback.
- For public services, restrict which interfaces are exposed and combine with network controls (firewall, private subnet, auth) rather than relying on the bind address alone.
- Confirm the current bind and default behavior of your framework and platform, since defaults differ across languages and hosting environments.
Caveat: The source notes the unsafe default surprised it; the specific default depends on runtime and version, so always verify.

Tags: bot-and-agent-security, deployment, network-security, secure-defaults
Source: Site Security (1).docx

---

## Add CSRF Validation Centrally for State-Changing Requests
Use when: Securing store forms and state-changing endpoints — checkout submission, cart mutation, account changes, admin actions.
- Implement a middleware that runs before every request and validates a CSRF token when the request is a state-changing method (e.g., POST).
- Apply it globally rather than per-route so no new endpoint forgets the check.
- Use the same layer for other cross-cutting checks (logging, token verification) and only pass the request onward when valid.
- Verify current framework guidance on token issuance, SameSite cookies and rotation, since these mechanisms evolve.
Caveat: The source mentions CSRF in passing as an example; it does not provide a complete CSRF implementation, and CSRF protection is one layer and not a full defense.

Tags: bot-and-agent-security, csrf, web-framework, checkout, authentication
Source: Site Security (1).docx

---

## Use Strongly Typed Checks to Force Exhaustive Case Handling
Use when: Choosing languages or tooling for store components that branch on request type, payment status or order state where missing a case is costly.
- Where the risk of an unhandled case is high (e.g., payment callbacks with many statuses), consider a strongly typed language that produces a compile-time error if a case is missed.
- Weigh the trade-off: the source acknowledges stronger typing can slow development and teams often choose loosely typed languages deliberately.
- If you stay in a loosely typed language, compensate with explicit runtime validation and tests covering each branch instead of clever introspection.
- Avoid hacky runtime introspection of source code (e.g., parsing a function's string form to check handling) — the source explicitly does not recommend it.
Caveat: The source frames strong typing as one possible mitigation and a trade-off, not a required choice.

Tags: bot-and-agent-security, language-choice, type-safety, code-review, payment-integration
Source: Site Security (1).docx

---

## Treat memory disclosure and uninitialized buffers as a storefront data-leak risk
Use when: Building or reviewing any storefront endpoint, agent tool, or middleware that returns request data, error dumps, or templated responses back to a browser.
- Classify any handler whose response body includes data assembled from request input, logs, or a shared pool as a potential disclosure path; do not assume a benign handler is safe because its logic looks read-only.
- Require that every response that echoes input is constructed only from fields you explicitly select; never stringify a raw network buffer, a pooled allocation, or a whole error object into the body.
- Verify buffers used for customer data are allocated zeroed or overwritten before use, and that serialization reads only the declared length rather than the backing allocation.
- Test on systems you own: send requests with canary strings in unused fields, then confirm the canary never appears in any other customer's response or in an error page.
- Apply the same rule to agent tool output and retrieved documents: treat them as untrusted data that can be surfaced to a user, not as content safe to paste back verbatim.
- Add a log/response review step: grep response bodies for long opaque strings and for values that resemble API keys, session tokens, or payment fields before go-live.

Tags: bot-and-agent-security, data-exposure, api-hardening, input-validation, logging, testing, pci-scope
Source: Site Security (1).docx

---

## User interaction before a sensitive local or remote action
Use when: Designing storefront or admin features that a browser could trigger without the customer's intent, such as store locators, device pairing, card-on-file actions, or integration callbacks.
- Identify every endpoint or integration action that changes state — firing an order, saving a payment method, pairing a device, running a refund — and ask whether a website could trigger it via a simple GET or form POST.
- Insert an explicit confirmation step (button, modal, or re-authentication) in the UI before the action executes; the source presents this as an acceptable mitigation for an over-permissive server.
- Keep the confirmation server-side meaningful: the confirmation must be tied to the authenticated session and to the specific action parameters, not a static token any page can reuse.
- For agent-driven flows, require a human approval step before the agent can invoke state-changing tools (refunds, price changes, publishing) unless the tool is read-only and scoped to the brand.
- Log the approval event with who approved, what parameters, and when, so disputed changes can be reconstructed.

Tags: bot-and-agent-security, approval-workflow, csrf, checkout, admin, audit-logging, agent-tools
Source: Site Security (1).docx

---

## Use non-simple requests as a defense in depth, not as the fix
Use when: Hardening a local or internal HTTP endpoint (device gateway, integration listener, admin service) that currently accepts simple GET/POST requests.
- Determine whether the endpoint currently accepts simple requests: methods GET/HEAD/POST with form content types, which any page can trigger without a preflight.
- Move sensitive state-changing actions to a method that requires a preflight (e.g., PUT/DELETE) or require a custom header, so the browser asks permission before sending.
- On the server, validate the request's origin against an allowlist in the preflight response; missing or non-matching origin should be denied rather than defaulted to allow.
- Do not treat a framework default that permits all HTTP methods as your control — the source shows Express-appeared-to-allow PUT while the browser still blocked the request because no explicit allow-origin was returned.
- Recognize the limits: non-browser clients (scripts, other apps) ignore preflight rules entirely, and DNS rebinding makes the request same-origin in the browser's view.
- Verify current CORS/preflight behavior for your framework and browser versions, since defaults and error messages change between releases.

Tags: bot-and-agent-security, cors, preflight, api-hardening, csrf, agent-tools, verification
Source: Site Security (1).docx

---

## Scope local-network and integration endpoints so a browser cannot reach them
Use when: Deploying device gateways, print/label services, POS bridges, or any ecommerce integration listener that runs on a store machine or local network.
- Inventory services that listen on localhost, RFC1918 addresses, or internal hostnames and are reachable from the browser — printers, label makers, scanners, POS bridges, dev servers, admin consoles.
- Prefer a protocol-handler / OS-registered deep link over a local HTTP server when the goal is only to launch a native app; this removes the attack surface entirely.
- If a local server is required, bind it to a specific interface and origin allowlist rather than all interfaces, and require authentication tokens the page cannot obtain cross-origin.
- Assume any device on the local network is untrusted and applies weak authentication: firmware is often frozen at factory state with no update path, so treat firewall placement as your primary control.
- Keep internal services off the customer's network segment or behind a tunnel/gateway so the browser cannot act as a proxy to them; use per-token scoping rather than network trust.

Tags: bot-and-agent-security, iot, network-segmentation, integrations, access-control, firewall, store-ops
Source: Site Security (1).docx

---

## Capabilities of a same-origin rebinding-style attack on storefronts
Use when: Assessing risk when store systems, fulfillment hardware, or admin consoles share a network with the customer's or staff's browsing environment.
- Map what a same-origin request from your own domain could reach: printers, label printers, scanners, smart speakers, routers, access points, POS bridges, dev servers, and admin panels.
- Prioritize routers, switches, and access points, since compromise there lets an attacker change DNS settings or proxy traffic for every device on the store network.
- Note that the browser enforces same-origin by scheme+hostname+port only; it does not bind the origin to a particular IP, so hostname-to-IP reassociation is the crux of the trick.
- Because simple GET/form-POST requests can still be sent, assume any local device accepting unauthenticated GETs is reachable by any page that loads on your network.
- Confirm that firewall rules block inbound connections from the internet; the browser acting as an internal proxy is what gets past that default.

Tags: bot-and-agent-security, threat-model, network-segmentation, iot, store-ops, firewall, risk-assessment
Source: Site Security (1).docx

---

## Keep access-control headers off endpoints that never meant to share data
Use when: Reviewing CORS configuration on local services, internal tooling, or storefront APIs that return customer, order, or token data.
- Remove wildcard Access-Control-Allow-Origin from endpoints whose responses are not meant for third-party pages; the source shows deleting the wildcard header stopped a page from reading a response while the request itself still went through.
- Understand the asymmetry: for a non-preflighted request, the browser sends the request first and only then decides whether the page may read the response, so blocking reads does not block the action.
- Therefore do not rely on read-blocking for state-changing endpoints — combine with method/origin restrictions, authentication, and an explicit approval step for sensitive actions.
- For endpoints that must be shared, return an explicit origin allowlist and only the methods and headers needed, and cache the preflight response with an appropriate max-age to limit overhead.
- Re-test after changes: source notes a fix can appear to work while remaining vulnerable, so validate with an owned test page rather than assuming the patch holds.

Tags: bot-and-agent-security, cors, api-hardening, data-exposure, verification, checkout
Source: Site Security (1).docx

---

## Use allowlist identity keys and reject unauthenticated state changes
Use when: Reviewing connected device integrations, IoT hardware, or admin endpoints that control physical or financial state in a store or customer environment.
- For every connected device or service, ask what happens if a fully untrusted caller sends the same request; if it changes temperature, prints, unlocks, or restarts, it is unsafe by default.
- Require authenticated, origin-bound requests for state changes rather than trusting that anyone on the network is friendly — the source notes many such devices assume local network equals trusted.
- Apply the same to non-browser callers: scripts and native apps ignore browser preflight rules, so browser-enforced controls can never be the sole defense for an endpoint with real-world effects.
- Include non-technical risk in the assessment: unauthenticated control of thermostats or similar devices can be dangerous to occupants and costly when the store or customer is away.
- Record which devices on the store network accept unauthenticated commands and prioritize replacing or isolating those that do.

Tags: bot-and-agent-security, iot, access-control, threat-model, store-ops, risk-assessment
Source: Site Security (1).docx

---

## Simple vs preflighted requests: which cross-site calls a page can make
Use when: Deciding which storefront or integration endpoint methods a hostile page could reach, and designing the method/content-type/header profile accordingly.
- Classify each endpoint: if it can be invoked by an img tag or a basic form (GET, or POST with form-encoded/multipart/text-plain), treat it as reachable by any page.
- For endpoints that must not be reachable cross-site, require a method or header that is not simple (e.g., PUT/DELETE or a custom header), so the browser must preflight.
- On the server, handle the preflight by returning an explicit allow-origin, allow-methods, and allow-headers; treat a server that doesn't support preflight as deny by default.
- Remember that even a refused preflight means the browser blocked the request, so an endpoint relying on this should also send a correct allow-origin rather than a permissive one.
- Recognize that this defense fails for non-browser clients and, as the source discusses, does not address DNS-rebinding-class attacks where the request appears same-origin.

Tags: bot-and-agent-security, cors, preflight, api-hardening, csrf
Source: Site Security (1).docx

---

## Treat agent- and browser-initiated requests as untrusted input, not authorization
Use when: Building checkout helpers, admin copilots, or automation that reads pages, emails, tickets, or vendor docs and can act on the store's systems.
- Separate the data channel from the action channel: retrieved content informs the agent, but only a scoped credential plus an approved action mapping can execute a refund, order, price change, or export.
- Scope every agent credential to the brand and to the minimum tool set needed for the current task; drop access to payment, pricing, or customer data unless the task explicitly requires it.
- Require an explicit, human-confirmed action record before any agent-initiated state change, with the request parameters and tool invocation logged.
- Do not let a fetched document or tool response name its own permissions, scope, or destination URL; validate those against your allowlist in code, not in the model prompt.
- For storefront pages, keep the same discipline the browser already enforces cross-site: pages cannot make complex cross-origin requests without the server's explicit consent, and that consent must not be delegated to content.

Tags: bot-and-agent-security, agent-tools, prompt-injection, access-control, approval-workflow, audit-logging
Source: Site Security (1).docx

---

## Give each listener its own port and verify the actual request on the wire
Use when: Debugging or reviewing an integration listener, local gateway, or webhook receiver that appears to accept requests but behaves unexpectedly.
- Ensure each listener binds a unique, intended port and hostname alias; mixing local and remote services on the same port causes requests to go to the wrong place, as seen when a local server and an attacker-side server both wanted 8080.
- When testing, open developer tools and confirm the actual method sent — found was OPTIONS instead of the intended PUT, meaning a preflight occurred and the real request never went out.
- Read response headers, not just status codes, and check the console message; error text such as a failed preflight makes it explicit the browser refused because no allow-origin was returned.
- When a fix appears to work, re-run the exact hostile case on owned systems; the source reports a fix that looked correct but left the service exploitable for months.
- Do not rely on framework defaults for method policy — verify current behavior against your framework version and the browser you are targeting.

Tags: bot-and-agent-security, cors, preflight, testing, verification, troubleshooting, api-hardening
Source: Site Security (1).docx

---

## Hostname-to-IP reassociation is the mechanism to explain in store risk reviews
Use when: Briefing engineers or vendors on why origin checks and allowlists alone do not protect local services, integrations, or connected devices in a store environment.
- Explain the mechanism as: the page is served under the attacker's hostname, then the DNS answer for that hostname is changed to a private address, so the browser believes the request never left that origin.
- Because the browser sees a same-origin request, it sends no preflight and applies no cross-origin read restriction regardless of method, headers, or payload complexity.
- Use this to justify defense at the target service (authentication, origin-independent validation, local binding) rather than relying only on browser-side checks.
- Note the practical scope from the source's survey: many commonly deployed device classes have been found vulnerable at some point, so assume unknowns rather than relying on device reputation.
- Keep DNS/hosts pinning and split-horizon DNS in the review, and confirm enterprise DNS settings rather than assuming caching alone prevents reassociation.

Tags: bot-and-agent-security, threat-model, dns, cors, integrations, iot, awareness
Source: Site Security (1).docx

---

## Validate the mitigation against non-browser callers too
Use when: Deciding whether an endpoint is actually safe when the threat model includes admin tooling, scripts, mobile apps, third-party integrations, or local automation.
- For each protected endpoint, ask what happens if a native script or another installed app sends the request directly; if it could succeed, the endpoint's protection is incomplete.
- Move the control to the server: require authentication, authorization-scoped tokens, and validation of the action itself, rather than relying on the browser to refuse the request.
- Apply least privilege to local integrations — a print bridge or label service should need only the permission to print, not general network access.
- Consider firewalling or isolating services on the store machine so a compromised local process has a narrow blast radius.
- Document residual risk explicitly: the source's stated position is that browser-side enforcement is real but not sufficient for endpoints with meaningful capabilities.

Tags: bot-and-agent-security, threat-model, access-control, api-hardening, least-privilege, store-ops
Source: Site Security (1).docx

---

## Prioritize router and network-device exposure in the store environment
Use when: Planning network security for a store or warehouse, or deciding what to harden first when local devices are in scope.
- Inventory the store's network gear by model and firmware version, including the customer-facing Wi-Fi and any shared hotspot; these devices are often the highest-impact target.
- Check for default or shared admin credentials and disable remote management on any interface reachable from the internet.
- Segment the network so store devices (POS, printers, label makers) sit apart from guest Wi-Fi and from browsing devices, limiting lateral movement after a device is compromised.
- Treat access to a compromised network device as sufficient to intercept or manipulate store traffic; plan monitoring and out-of-band alerting for configuration changes.
- Apply vendor firmware updates on a schedule and re-check after updates, since the source's stated experience is that fixes can be incomplete or silently ineffective.

Tags: bot-and-agent-security, network-segmentation, iot, firewall, store-ops, risk-assessment
Source: Site Security (1).docx

---

## Monitor inbound reachability and device updateability on the store local network
Use when: Reviewing store or warehouse network policy, onboarding new IoT hardware (printers, cameras, displays), or responding to a suspected local-device compromise.
- Confirm the firewall defaults deny unsolicited inbound connections from the internet to every listening device, printer, camera, or service on the store LAN.
- Verify outbound-initiated connections are still allowed, since some mitigation approaches (tunnels, push-based integrations) rely on the device initiating outbound rather than accepting inbound.
- Track which devices have a supported update path and which are effectively frozen; for the latter, isolate them and remove unneeded capabilities.
- Recognize that a printer or camera compromise alone may not be the objective — it is a pivot point for moving through the network, so segmentation and egress rules matter.
- Re-test after network changes; the source reports bugs and incomplete fixes persisting even after people believed the device was corrected.

Tags: bot-and-agent-security, iot, firewall, network-segmentation, risk-assessment, testing
Source: Site Security (1).docx

---

## DNS Rebinding: How an Attacker Turns a Visitor's Browser into a Proxy for Your Local Services
Use when: Auditing store hardware, local sync utilities, label printers, or any locally-hosted admin service that your ecommerce staff run on machines also used for web browsing.
- Understand the pattern as a sequence: an attacker page loads from a domain the attacker controls and resolves to the attacker's own server; then the attacker changes the DNS record for that same domain to point at a loopback or LAN address; the page's JavaScript then issues a request to that same attacker hostname, the browser re-resolves, and the request lands on a machine on the visitor's own network.
- The browser treats the request as same-origin because the scheme, hostname and port in the URL did not change, even though the IP the request actually reached changed completely. Same-origin policy is defined on hostname, not on IP address, so a DNS flip is invisible to it.
- Recognize why local services are the high-value target: they typically assume that anyone who can reach them is on the same trusted network, so they often lack authentication entirely. A printer, a smart plug, or a locally running helper daemon may accept commands from anything that can open a connection.
- In real attacks the visitor does not click a button; the page retries the request on a timer (the source describes roughly every ten seconds) to outlast DNS caching. Keep-alive is countered by requesting connection close so the browser must re-resolve and open a new socket.
- Take the practical lesson for store operations: any web-connected device or local utility that accepts unauthenticated commands is in scope, and you cannot rely on the network boundary alone because the browser sits on the trusted side.
Caveat: Attacker-side operational detail is included only to explain the vulnerability class; the defensive conclusion is that unauthenticated local services are unsafe regardless of network placement.
Caveat: Browser DNS caching behavior, keep-alive defaults and resolver caching policies vary and change over time; verify current behavior rather than assuming the source's described timings.

Tags: bot-and-agent-security, network-security, dns-rebinding, iot, local-server, threat-modeling, same-origin-policy
Source: Site Security (1).docx

---

## Host Header Validation: The Standard Server-Side Defense Against DNS Rebinding
Use when: Hardening any locally running service, device API, or integration helper that your store operates and that is reachable from a browser on the same machine or network.
- Read the Host header on every inbound request. The Host header states which site the request is intended for, and it is the one part of the request that reflects what the browser believes it is talking to rather than the URL path.
- Compare it against the exact hostname (and port, if applicable) that the service expects, such as the loopback name plus its listening port. A request carrying an external attacker hostname is the signature of a rebinding attempt.
- Reject mismatches before routing: throw an error, return a 4xx, or destroy the socket without producing a body, so the browser gets no useful response.
- Implement the check once as middleware that runs before all handlers, rather than duplicating it into each handler, so new endpoints are covered automatically and a future handler cannot forget it.
- Validate by reproducing the attack on systems you own: point a test DNS entry at the local address, issue the request, and confirm the server refuses it while normal loopback traffic still succeeds.
Caveat: Do not confuse the Host header with the Origin header. The source describes a real case where a check was placed on the Origin path and merely suppressed a CORS response header instead of closing the connection; the service stayed vulnerable for months because the connection was still processed.
Caveat: Sending a deny response rather than terminating the connection may still let some handlers act; the source's later, correct fix was to close the socket immediately on Host mismatch.

Tags: bot-and-agent-security, dns-rebinding, host-header, local-server, input-validation, defensive-coding
Source: Site Security (1).docx

---

## Host vs Origin Headers: Keeping the Two Checks Straight in Store Integrations
Use when: Reviewing the request-validation code of an ecommerce integration, local print/sync agent, or any service that exposes an HTTP API to browsers.
- Treat the Origin header as the identity of the initiating page: it answers 'which site is making this request'. It is the basis for CORS allow-list decisions.
- Treat the Host header as the destination identity: it answers 'which server is this request addressed to'. It is the basis for DNS rebinding detection.
- When defending against rebinding, the control must act on Host. If Host does not match the expected local hostname, the connection should be terminated — not merely added to an allow/deny origin calculation, because a failed origin check may only omit a response header while the request still executes.
- When relaxing CORS for a legitimate first-party front end, be deliberate about which origins you allow, and recognize that CORS response headers do not stop a rebinding request that never needed CORS in the first place (it looked same-origin).
- Write the check at the very top of the request lifecycle so no later handler can run on a mismatched Host.
Caveat: This distinction was the exact source of a bug in a real project the source cites, where an adequate-looking fix failed in testing and shipped broken; test the negative case, not just the happy path.

Tags: bot-and-agent-security, dns-rebinding, host-header, origin-header, cors, input-validation
Source: Site Security (1).docx

---

## Reduce the Local-Server Attack Surface Before Adding Detection
Use when: Designing or reviewing desktop companion apps, in-store device software, POS helpers, or any product that spins up a listener on the operator's machine.
- Ask whether a local server is needed at all, and be willing to argue hard against shipping one. The source's recommendation is to avoid it if possible because the class of mistake is common and easy to get wrong.
- If one is required, bind the listener to the loopback address rather than all interfaces, so connections from other machines on the network are refused at the socket level.
- Recognize that OS firewalls that prompt for inbound connections do not protect against rebinding, because the browser making the request runs on the same host and the traffic never crosses the interface being filtered.
- Inventory every local service your software starts, including ones that feel incidental, and document the commands each accepts and whether they are authenticated.
- Prefer authenticated, token-gated access over network-position trust for any local service that can change data or execute code.
Caveat: Loopback binding and OS firewalls reduce but do not eliminate risk; the source is explicit that these defenses do nothing against a browser acting as a proxy on the same machine.
Caveat: Some legitimate functionality depends on a local server — the source describes a torrent client serving media to a local browser player — so removal is a trade-off, not a blanket rule.

Tags: bot-and-agent-security, local-server, attack-surface, pos, iot, defensive-architecture
Source: Site Security (1).docx

---

## Rebinding Against Remote HTTPS Sites Is Largely Blunted by TLS and Cookies
Use when: Prioritizing which of your assets need rebinding protection: ranking local unauthenticated services above public HTTPS storefront endpoints.
- Walk through the outcome when the flipped record points at a public HTTPS destination: the browser still believes it is talking to the attacker hostname, so the certificate presented for the real site's domain does not match and the connection is blocked.
- Even on plain HTTP targets, cookies are keyed to hostname: the browser attaches the attacker hostname's cookies, not the target's, so the request arrives unauthenticated and cannot act as the logged-in user.
- Conclude that the attacker gains little against a remote site, since they could have sent the same request themselves unless they can obtain the victim's ambient credentials.
- Apply this reasoning in triage: prioritize services that assume 'anyone who can reach me is trusted' — local daemons, network devices, admin panels bound to a LAN address — rather than those requiring authenticated sessions over TLS.
Caveat: The source frames this as why the remote-site case is 'not a big deal' relative to the local case; it is a limitation of the attack, not a reason to skip TLS or cookie hygiene.
Caveat: This reasoning assumes current browser certificate-validation and cookie-scoping behavior; verify current browser behavior for your own test cases.

Tags: bot-and-agent-security, dns-rebinding, tls, cookies, risk-prioritization, threat-modeling
Source: Site Security (1).docx

---

## Resolver-Level Mitigation: Refusing DNS Answers That Point to Loopback or Private Ranges
Use when: Configuring network policy for a store's office, warehouse or back-of-house networks where unpatched devices live alongside browsing machines.
- Identify the resolver your network clients actually use — the endpoint on each machine, the router, or the ISP resolver — because that is where the filter must be applied.
- Filter returned A/AAAA answers that point to loopback addresses, which map to services on the requesting device itself.
- Also filter private ranges. The source notes that it is not enough to block only loopback, because private address blocks used by local devices can be iterated just as easily; cover all of the private ranges your network uses.
- Recognize this as a network-wide control appropriate where you cannot patch or audit every device, which the source describes as the motivation enterprises have for it.
- Validate on an owned test network by resolving a hostname you control to a loopback value and confirming the resolver drops or rejects the answer.
Caveat: This is a resolver-side control; it does not fix a service that lacks Host validation, and it does not help traffic resolved by an external or client-side resolver you do not govern.
Caveat: It is not a substitute for the server-side Host check, which remains the control that travels with the software.

Tags: bot-and-agent-security, dns, network-policy, dns-rebinding, iot, defensive-architecture
Source: Site Security (1).docx

---

## Caching and Keep-Alive Timing Determine Whether Rebinding Succeeds at All
Use when: Assessing residual risk from rebinding for a device or integration and deciding how confidently to claim a fix works.
- Note that the request must land after the attacker's DNS record has propagated and after the browser's cached answer has expired. The source describes attackers setting very short TTLs and retrying periodically so they eventually hit the right window.
- Account for intermediary caches: recursive resolvers and ISP resolvers may impose a minimum cache time longer than the record requests, which can delay the attack considerably or defeat it in some networks.
- Account for connection reuse: if the browser keeps a TCP connection alive, no new DNS lookup occurs and the flipped record never takes effect. Blocking or refusing keep-alive forces re-resolution.
- Use this variability when validating a control: a single successful or failed test is not conclusive. Repeat the test across a time span that exceeds your resolver's cache behavior.
- Do not treat the attack's unreliability as a defense — a patient attacker with a retry loop waits out the cache.
Caveat: Concrete cache durations, minimum-TTL policies and keep-alive defaults vary by browser, resolver and platform, and are subject to change; treat the source's second-to-minute timescales as illustrative.

Tags: bot-and-agent-security, dns-rebinding, dns, caching, keep-alive, test-design
Source: Site Security (1).docx

---

## Real DNS Rebinding Incidents Show the Blast Radius: Update Agents and Background Daemons
Use when: Assessing your own desktop software, updater, or background service for the same class of flaw before shipping or renewing a security review.
- Look for local HTTP servers started by updaters and companion apps. The source describes a game update agent that ran a local server accepting commands to download and execute binaries, which meant any website the user browsed could trigger execution.
- Look for split-process architectures where a UI process talks to a background worker over HTTP on a local port. The source cites a torrent client whose worker accepted executions from anything that could connect, not just its own UI.
- For each such service, enumerate every endpoint that changes state or executes anything, and ask whether it authenticates the caller rather than trusting the connection's apparent origin.
- Apply the Host check you would apply to any local server, and additionally add authentication for anything privileged so a rebinding attempt cannot succeed merely by guessing the port.
- When you fix such an issue, test the actual negative case end to end; the source recounts a fix that looked correct in testing and left the service exposed for about six months until someone re-found it.
Caveat: These are cited real-world cases, not guarantees about any specific vendor's current software; verify the present state of any tool before relying on it.
Caveat: Do not assume a local service is safe because its port is obscure; the source notes port ranges are enumerable by a page left open long enough.

Tags: bot-and-agent-security, dns-rebinding, local-server, updater, vulnerability-management, desktop-software
Source: Site Security (1).docx

---

## Mirai as an Ecommerce-IoT Cautionary Case: Default Credentials and Internet-Facing Device Ports
Use when: Procuring any internet-connected device for a store — cameras, signage players, smart plugs, routers, thermostats — or drafting requirements for connected-device purchases.
- Treat default credentials as a procurement-blocking defect. The source highlights devices shipping with administrative passwords set to trivially guessable defaults and attackers trying them directly.
- Treat an internet-reachable management port as a design defect. Many devices listened on all interfaces with no firewall, so attackers connected directly without needing rebinding at all.
- Recognize why updates lag: consumer price pressure means little security scrutiny at purchase and infrequent firmware updates after shipment, so assume the device's security posture is frozen.
- In a store deployment, put management interfaces behind a separate network segment with no inbound path from the public internet, and change credentials before the device carries any real traffic.
- Include 'no default credentials, updatable firmware, no unnecessary listening services' in purchase criteria rather than evaluating only price and features.
Caveat: The source recounts the botnet's origin story and its targeting-avoidance choices as background color, not as technical guidance; the transferable lesson is the device-side hygiene, not the operational history.
Caveat: The source's remark that the 'S' in IoT stands for security is a presenter's joke about market incentives, not an evaluated claim.

Tags: bot-and-agent-security, iot, default-credentials, network-segmentation, procurement, botnet
Source: Site Security (1).docx

---

## Bound Session Reuse of Local Admin Tools in Store Operations
Use when: Setting up in-store workstations, POS terminals, or back-office machines that use both web admin panels and general web browsing.
- Separate browsing from device administration. Put device and appliance management interfaces on a dedicated machine or dedicated browser profile that is not used to visit arbitrary external sites.
- Where a single machine must do both, restrict outbound browsing for that machine so an attacker page cannot be reached in the same session as the admin interface.
- Audit which locally running services accept requests without authentication, since those are the ones a rebinding page can reach regardless of the network path.
- Treat any admin panel on a store workstation as exposed to every website the operator visits, not merely to the local network.
- Log and review access to device management endpoints so unexpected requests from a browser session stand out.
Caveat: This is a source-derived operational practice built on the source's rebinding explanation; it is not a demonstrated case study from the source.

Tags: bot-and-agent-security, pos, browser-security, network-segmentation, device-management, operational-hygiene
Source: Site Security (1).docx

---

## Browser Engine Bugs Let Merely Visiting a Page Compromise the Machine
Use when: Deciding how much general web browsing to permit on machines that handle customer data or payment-adjacent operations.
- Understand the mechanism at a high level: a language-level property, implemented as a getter, can report a buffer length far larger than the memory actually allocated when native code reads that property, producing an out-of-bounds read and write primitive.
- Recognize that this class of flaw is exploited from ordinary untrusted pages, so no plugin, download or user consent is needed — the visit itself is the trigger.
- Apply it operationally: browsers are large, network-facing codebases frequently written in memory-unsafe languages and continuously gaining features, so assume defects exist and reduce time spent browsing untrusted sites on sensitive machines.
- Prefer keeping browsers updated promptly, since many such flaws are fixed by vendor patches, and treat patch currency as a control rather than a formality.
- Where possible, constrain which sites a store operations browser can reach, since only permitting known destinations removes most of the exposure.
Caveat: This is presented as a historical demonstration, not a claim about any current browser version; do not cite it as a present-day vulnerability.
Caveat: The source frames such exploits as having become less common after browser architecture improvements, not eliminated.

Tags: bot-and-agent-security, browser-security, memory-safety, malware, workstation-hardening, patching
Source: Site Security (1).docx

---

## Assume Breach at the Browser Layer and Design Store Systems for Containment
Use when: Architecting access for ecommerce back office, order management and payment tooling where staff use web browsers all day.
- Assume that a machine used for browsing untrusted sites may be fully compromised, and design downstream access accordingly rather than relying on endpoint trust.
- Require re-authentication or a second factor for high-impact actions such as exporting customer records, changing payout or bank details, or bulk-editing prices, so stolen session material alone is insufficient.
- Scope administrative permissions per person and per role, so a compromised session holds only the privileges that operator actually needs.
- Keep high-privilege admin surfaces on separate accounts and separate browser profiles or machines from day-to-day browsing.
- Log privileged actions with actor and source information so anomalous activity from a normally low-traffic workstation can be detected.
Caveat: This is a defensive inference drawn from the source's browser-attack material rather than a procedure the source itself prescribes; treat it as risk reduction, not a guarantee.
Caveat: Additional factors and least privilege do not stop a compromise of a privileged session that has itself been authenticated.

Tags: bot-and-agent-security, least-privilege, browser-security, access-control, logging, back-office
Source: Site Security (1).docx

---

## Run a Bounded Rebinding Test Against Your Own Local Service
Use when: Validating a fix to an updater, device API, or local companion service before shipping it or closing out a security finding.
- Stand up the service on a machine you own, and craft a request whose Host header names an external hostname rather than the service's own hostname, simulating what a browser would send after a DNS flip.
- Observe whether the service refuses the request. Confirm that the connection is terminated and no handler executes; a response that merely omits a CORS header is not a pass.
- Confirm the legitimate path still works: a request carrying the expected local hostname must be processed normally, so the control is not simply breaking functionality.
- Repeat the test with the request issued from a page that could plausibly originate it, so you exercise the same code path a browser would.
- Re-run the test after later refactors, since the source's own example shows a fix that appeared correct in testing yet remained exploitable for months.
Caveat: Perform this only against systems you own or are explicitly authorized to test; the underlying technique is offensive and must not be pointed at third-party services.
Caveat: Do not generalize a pass from one endpoint to the whole service; unlisted endpoints may bypass middleware that was added later.

Tags: bot-and-agent-security, dns-rebinding, test-design, host-header, validation, local-server
Source: Site Security (1).docx

---

## Enforce the Host Check at the Very Top of the Request Pipeline
Use when: Implementing or reviewing request-validation middleware for any store service, integration endpoint or local device API.
- Identify the earliest point in the request lifecycle that runs for every request, and place the reject-on-mismatch logic there.
- Reject by destroying the socket or returning an error immediately, so no downstream handler and no response body processing occurs.
- Avoid nesting security checks inside helpers whose failure path has a different meaning — for example, an allow-list helper whose false return only suppresses a response header rather than denying the request.
- Write a test that asserts the specific negative outcome you intend (connection closed, no side effect), not merely that some response was returned.
- Review each new endpoint against the single top-level guard, rather than waiting for each handler author to add their own.
Caveat: Middleware ordering assumptions can change as frameworks are upgraded; verify the guard still executes first after dependency updates.
Caveat: A correct guard still requires the service to be bound and exposed appropriately; it is one layer, not the entire defense.

Tags: bot-and-agent-security, defensive-coding, middleware, host-header, dns-rebinding, code-review
Source: Site Security (1).docx

---

## Decide How Much Local-Server Functionality Your Product Actually Needs
Use when: Prioritizing which local-service features to keep, redesign, or retire in store software and companion apps.
- List the concrete user-facing capabilities that require a local listener, such as serving media to a browser player or letting the UI control a background worker.
- For each, ask whether the same capability can be delivered without a listener — an OS-level integration, an in-process call, or a server-side flow — before accepting the risk.
- Where the listener is necessary, constrain what it accepts to the narrowest command set possible, and add authentication on top of the Host check rather than relying on either alone.
- Make the hostname the service expects an explicit configuration value so the guard can compare against a known expected value rather than a hardcoded assumption that may drift.
- Record in your documentation that the local listener exists and why, so future teams do not silently expand its capabilities.
Caveat: The source's stance is that local servers are risky and should be avoided where possible; it also acknowledges legitimate uses, so treat this as a weighted trade-off rather than a blanket prohibition.

Tags: bot-and-agent-security, local-server, product-design, attack-surface, host-header, risk-tradeoff
Source: Site Security (1).docx

---

## Renderer/browser process separation to limit storefront breach damage
Use when: Architecting or reviewing the security boundaries of a custom storefront, headless-rendering service, or in-house checkout so a rendering bug cannot touch customer data or admin files.
- Apply the source's 'rule of two' heuristic defensively: code that (1) processes untrusted input, (2) is written in an unsafe/memory-unsafe language, and (3) runs with privileged permissions should be avoided — any single component doing all three is high-risk. The source credits Chrome with popularizing this framing; treat it as a design heuristic, not a hard rule.
- Split your system: put complicated parsing of untrusted content (product images, CSV feeds, user-supplied HTML, JS-heavy widgets) into a low-privilege process or sandbox that has no direct disk, network, or credential access.
- Keep the sensitive operations (reading customer records, session cookies, payment tokens, admin files) in a separate privileged process. The low-privilege side must request these over an explicit IPC channel that the privileged side can refuse.
- Label each IPC channel by the origin/tenant it serves, so a compromised renderer can only request data it legitimately owns (the site-isolation principle).
- Assume the low-privilege process WILL be compromised and deny it cookies, tokens, and files belonging to other origins or customers; enforce cross-origin read blocking server-side so foreign HTML is not delivered into an untrusted renderer as data.
- Verify current sandboxing, site-isolation and header behavior against your platform's present documentation before relying on specific defaults.
Caveat: The source notes limitations: prior multi-site-per-tab designs put multiple origins in one process, weakening isolation, and Spectre-class CPU attacks can cross process boundaries — process isolation alone is not a guarantee.
Caveat: Some flexibility is intentional: cross-origin images and CORS-permitted responses may still need to load. Do not block all legitimate cross-origin asset loading.

Tags: bot-and-agent-security, storefront-architecture, sandboxing, defense-in-depth, session-security, integration-security
Source: Site Security (1).docx

---

## Defend against memory-safety bugs as the dominant vulnerability class
Use when: Selecting a stack or writing parsers/decoders for untrusted store inputs (images, feeds, uploads, custom widgets) on a storefront or checkout service.
- Recognize that the source reports memory-safety issues dominate critical browser bugs (a Microsoft stat cited ~70% of yearly patched vulns; Chrome reportedly ~130 critical bugs of which only ~5 were non-memory-corruption). Treat these as directional, time-bound figures, not current benchmarks.
- For any new service that parses untrusted content (image/PDF decoders, feed parsers, user-upload handlers), prefer memory-safe languages (Rust, Go, managed runtimes) where the platform prevents buffer overruns if implemented correctly.
- Where you must keep C/C++ components (existing CDN edge code, native image libraries), wrap them in a low-privilege sandbox and give them no direct access to credentials, customer DBs, or the order system.
- Route all untrusted-input parsing through an isolated worker so a decoder bug cannot reach the payment or account service.
- Track memory-safety advisories for your native dependencies and patch promptly; auto-updating these components is a strong control.
- Verify current language/runtime guarantees with the vendor rather than assuming a language is automatically safe.
Caveat: Memory-safe languages reduce but do not eliminate risk if the runtime itself has bugs; the source emphasizes correctness of the runtime matters.
Caveat: The cited percentages are from the source's era and should be re-checked against current data before quoting.

Tags: bot-and-agent-security, memory-safety, input-parsing, language-selection, sandboxing, upload-handling
Source: Site Security (1).docx

---

## Enforce strong auto-update for storefront dependencies
Use when: Designing update policy for a storefront, an in-store kiosk browser, an embedded widget, or a dependency pipeline.
- Adopt Chrome's precedent (per the source, initially controversial): make security updates automatic and on by default rather than prompting users, because outdated versions are a primary attack vector.
- For customer-facing or kiosk browsers running your checkout, configure silent auto-updates so a device cannot linger on an old vulnerable build.
- Build an update mechanism early — the source notes Chrome's project literally started as an auto-updater with a blank window before any browser features existed, so treat update infrastructure as a first-class dependency, not an afterthought.
- For your dependency tree, pin versions but run automated vulnerability scans and PR bots so patches flow quickly; do not freeze indefinitely on an old package set.
- Retire or block access from unsupported old client versions to reduce the population of vulnerable clients hitting your endpoints.
- Verify the current auto-update configuration interfaces for your browser/OS, as these change over time.
Caveat: Auto-update can introduce regressions; the source treats forced updates as standard practice now but acknowledges it was once controversial.
Caveat: Deleting old binaries (as the source says Chrome does) may conflict with a need to support legacy clients — decide per store.

Tags: bot-and-agent-security, patching, dependency-management, kiosk-security, update-policy
Source: Site Security (1).docx

---

## Use browser isolation and separate sessions for ecommerce administration
Use when: Running multi-tenant embeddable storefronts, marketplaces, or iframe-based checkout widgets where one origin could attack another.
- Keep administrative browsers and embedded runtimes patched with supported sandbox and isolation features.
- Separate privileged store administration from untrusted browsing and avoid sharing privileged sessions with automated content collection.
- Inventory embedded third-party content and restrict permitted origins and capabilities.
- Test integration behavior under supported security defaults instead of disabling sandboxing to make a widget work.
Caveat: The lecture's renderer and IPC architecture is browser-engine context; a storefront cannot directly implement those process guarantees.

Tags: bot-and-agent-security, site-isolation, multi-tenant, cross-origin, iframe-embeds, session-security
Source: Site Security (1).docx

---

## Harden JavaScript for storefront and checkout code
Use when: Writing or reviewing checkout, cart, pricing, or order-API JavaScript that handles user-submitted JSON and query data.
- Enable strict mode ('use strict') or the module equivalent at the top of files to convert silent errors into thrown exceptions — e.g. undeclared variables no longer leak into globals, and duplicate parameter names become syntax errors.
- Always use strict equality (===) instead of ==, because the source warns that the abstract equality comparison algorithm coerces types unintuitively (e.g. a check for 0 can match multiple values).
- Adopt a linter — the source recommends ESLint and its own 'standard' preset — configured to catch duplicate object keys (which strict mode cannot catch), accidental octal literals, and unused/unreachable code. The source adds that standard ships an auto-fixer for issues like swapping == for ===.
- Guard against prototype pollution: when accepting user JSON for pricing, cart items, or filters, never trust property names like hasOwnProperty. Use Object.prototype.hasOwnProperty.call(obj, key) or Object.create(null) so a malicious key cannot override inherited methods and crash the order service.
- Treat all incoming JSON/query parameters as untrusted; validate and sanitize before they reach pricing or order logic.
- Verify current linter rule names and presets, as these change between releases.
Caveat: The source notes some bugs (like duplicate object keys) cannot be caught by strict mode and require a linter.
Caveat: Linting is source-recommended, not a guarantee; it reduces but does not eliminate vulnerabilities.

Tags: bot-and-agent-security, javascript-security, input-validation, prototype-pollution, linting, checkout
Source: Site Security (1).docx

---

## Defend against automatic semicolon insertion pitfalls in storefront scripts
Use when: Writing or reviewing storefront, cart, or analytics JavaScript that mixes lines without semicolons or returns objects from functions.
- Understand that JS automatic semicolon insertion can reinterpret a line break as a continuation: a new line starting with '(' can become a function call on the previous line, and a line starting with '[' can become an array index, producing unintended results.
- Do not assume adding semicolons everywhere fully protects you — if a return is split across lines with the object on the next line, ASI can insert a semicolon after return, making an object-literal line dead code that silently does nothing. The source calls ASI a recognized mistake in the language.
- Run a linter configured to warn about unreachable/dead code and the ASI edge cases, since the source says the linter catches these whether or not you write semicolons.
- If you follow a no-semicolon style, adopt the practice of prefixing semicolons only on lines that begin with the handful of leading characters (such as '(' and '[') that trigger ASI re-interpretation.
- Spot-check that functions returning objects or arrays in pricing/cart logic actually return them, by testing the return value rather than reading the code.
- Confirm current linter rule availability, as rules evolve.
Caveat: The source states no style fully prevents ASI issues without a linter; writing semicolons everywhere is not a complete fix.

Tags: bot-and-agent-security, javascript-security, linting, code-quality, cart
Source: Site Security (1).docx

---

## Prefer explicit, boring code over clever code in security-relevant paths
Use when: Reviewing or writing checkout, pricing, authentication, or order-processing code where readability and auditability matter more than brevity.
- Reject code that requires all of the author's intelligence to parse — the source argues that cleverness later becomes unmaintainable even for the original author when context is lost.
- Replace short-circuit side effects (e.g. `foo && bar()`) with an explicit if-statement, so everyone on the team understands the intent, especially beginners and future maintainers.
- Avoid one-liners that combine spread syntax, conditionals, and object spread to build request payloads; the source demonstrates that even experienced readers mis-parse spread/operator precedence. Write an explicit object-build instead.
- Do not use obscure prototype methods for common tasks like trimming whitespace on a list of names — use the straightforward readable form.
- Keep dangerous operations visually dangerous: give risky functions scary names, document them, and do not bundle them in files with benign utility code, so reviewers see the risk.
- Reserve esoteric features for cases with clear, measurable benefit; the source treats this as a taste/preference issue rather than an absolute rule.
Caveat: The source frames this partly as a preference; some teams legitimately value dense functional style. It is not a hard security rule, though it reduces the chance of hidden bugs.

Tags: bot-and-agent-security, code-quality, secure-coding, review-practices, checkout
Source: Site Security (1).docx

---

## Protect against the open-source and extension supply chain
Use when: Choosing dependencies for a storefront platform, adding a browser extension to your workflow, or assessing third-party scripts and widgets on product pages.
- Acknowledge the source's framing: installing dependencies is effectively running code from many unknown, often unpaid volunteers on the same machine that holds business data.
- Classify supply-chain risk into three categories the source names: (1) accidental maintainer mistakes, (2) unmaintained/under-maintained packages, and (3) deliberate malice (rogue maintainer or compromised account).
- Reduce dependency count and tree depth where practical; each transitive package is an implicit trust decision.
- Vet third-party storefront scripts and payment/analytics widgets: check who maintains them, whether they are still active, and whether they are pinned.
- Be cautious with browser extensions in your operations team's browsers — the source warns popular extensions are sometimes sold to buyers who then add malware or track browsing, because extensions are hard to monetize. Audit or restrict extensions on admin/back-office machines.
- Keep backups: the source cites an install script that mistakenly ran a delete command wiping a user folder — backups are what saved victims.
- Continuously scan the tree (SCA tooling) and track advisories rather than assuming 'it works' means 'it is safe'. Verify current tooling behavior before relying on it.
Caveat: Even careful review cannot fully audit thousands of packages; risk is reduced, not removed.
Caveat: The source's specific incident counts and examples are historical illustrations, not current metrics.

Tags: bot-and-agent-security, supply-chain, dependency-management, third-party-scripts, extensions
Source: Site Security (1).docx

---

## Recognize targeted dependency attacks and account-takeover risk
Use when: Evaluating package maintainer activity, structuring a dependency policy, or investigating a suspicious release in your build pipeline.
- Watch for 'helper takeover' patterns the source describes: a maintainer is asked by a stranger to help with an abandoned but still-popular package and grants publish rights. Treat sudden publishing-rights transfers or maintainer changes on a critical dependency as a trigger for review.
- Detect exfiltration-style payloads: the source describes malware hidden as an encrypted string decrypted at runtime and evaluated, with a decryption key derived from the parent package in the tree, so it only ran for one targeted victim. This means generic antivirus or code review may miss it — behavior at runtime is the real risk.
- Pin exact versions and lockfiles, and review lockfile diffs so an unexpected version bump or new transitive package is visible before deploy.
- Run installs in isolated CI containers without production credentials so a malicious install script cannot read secrets, and restrict postinstall/install scripts where your package manager allows it.
- Consider reviewing or disabling install scripts in CI and running builds in a sandbox with no access to customer data or payment keys.
- Monitor advisories and maintainer activity for critical packages; verify current package-manager and CI isolation capabilities as they change.
Caveat: Targeted attacks may be undetectable by static analysis; the source's cited event-stream-style incident worked because the malicious code did nothing for most users. The described technique is historical — current attack patterns may differ.
Caveat: The source does not claim any single tool guarantees safety.

Tags: bot-and-agent-security, supply-chain, dependency-management, ci-isolation, secret-handling, targeted-attacks
Source: Site Security (1).docx

---

## Apply defense-in-depth and a paranoid mindset to storefront security
Use when: Designing overall security posture for a store account, checkout, admin panel, or integration layer.
- Treat all user input as untrusted and sanitize/validate it at every entry point (search, signup, review submission, order notes, file uploads).
- Layer defenses so that if one fails another still holds — the source explicitly recommends redundant 'defense-in-depth' rather than relying on a single gate.
- Hash and salt passwords; the source's direct advice is to use bcrypt rather than rolling your own. (Distinguish hashing from encryption and signing; hashing is for stored credentials.)
- Address ambient authority: browsers automatically attach cookies to requests destined for a site, which can leak them. Use SameSite cookies to constrain this, as the source recommends. Verify current SameSite values and browser defaults, which have changed over time.
- Adopt an attacker's mindset: when reading your own or a teammate's code, ask where inputs aren't what you expect and how the code could be broken, then fix those paths.
- Make dangerous code visibly dangerous — scary names, documentation, and no mixing with benign utilities — to reduce accidental misuse.
- Treat retrieved documents and tool/site output as untrusted data, not as authorization; scope any agent's access to the specific brand and task.
Caveat: The source notes no single control (HTTPS, hashing, CAPTCHA, WAF, filters) is sufficient alone; these are layers, not guarantees.
Caveat: Different frameworks now provide these primitives differently; verify current implementation details.

Tags: bot-and-agent-security, defense-in-depth, password-storage, input-validation, samesite-cookies, account-security
Source: Site Security (1).docx

---

## Write tests because untested code is broken code
Use when: Shipping any storefront feature where a silent bug would cost revenue — pricing, discounts, tax, cart totals, order submission.
- Treat 'it looks fine' as insufficient — the source flatly states that if you just write code and look at it, it is probably not good.
- Write tests covering the money-critical paths: pricing rules, discount stacking, cart totals, tax/shipping calculation, and order submission.
- Include edge cases the source's language warnings imply: type-coercion surprises, malformed user JSON, duplicate keys, and boundary values on quantities.
- Automate tests in CI so a supply-chain update or dependency bump that breaks behavior is caught before deploy.
- Combine tests with linting/static analysis — the source presents linters and tests as complementary quality controls, not substitutes.
- When reviewing a teammate's clever one-liner, ask for the test that proves its behavior, since cleverness hides intent.
Caveat: Tests reduce but do not eliminate risk; the source treats testing as critical, not sufficient on its own.

Tags: bot-and-agent-security, testing, ci, checkout, pricing, code-quality
Source: Site Security (1).docx

---

## Store passwords with a maintained adaptive password hasher
Use when: Reviewing how your store platform, custom app or admin panel stores customer and staff login credentials.
- Prefer the maintained identity system or framework password hasher over custom cryptography.
- For new implementations evaluate current Argon2id guidance and platform support; retain a planned migration path for legacy bcrypt hashes.
- Let the library manage salts and encoded parameters; a salted fast SHA hash is not a substitute for an adaptive password hasher.
- Benchmark safe cost settings against login capacity, rate limits and current guidance.
- Verify using the library API and rehash on successful login when the stored format needs upgrading.
Caveat: Algorithm requirements can differ by platform or compliance context. Password hashing does not stop credential reuse, phishing or a compromised login endpoint.

Tags: bot-and-agent-security, authentication, password-storage, cryptography, customer-accounts, admin-access
Source: Site Security (1).docx

---

## Ambient Authority via Cookies: Use SameSite
Use when: Hardening cookie-based sessions for your storefront, customer accounts or admin panel so other sites cannot silently trigger authenticated requests.
- Understand 'ambient authority': the browser automatically attaches a site's cookies to requests destined for that site, so a request from another page can arrive already authenticated as your logged-in user.
- This is the mechanism behind cross-site request forgery for state-changing actions — a logged-in shopper or admin visiting another page could have requests fired at your site carrying their session.
- The source's stated solution is SameSite cookies: configure your session cookies with a SameSite attribute (typically Lax or Strict) so the browser withholds them on cross-site requests.
- For state-changing endpoints — add-to-cart changes, address updates, payment or refund actions, admin mutations — consider requiring an explicit per-request token in addition to the session cookie, since SameSite policy and browser behavior can vary. Verify current browser SameSite defaults for your supported browsers.
- Test the flows that legitimately need cross-site cookies (for example a payment provider returning to your site) before tightening the attribute, or you may break checkout.
Caveat: Cookie attributes and browser SameSite defaults have changed over time and between browsers; verify against current browser documentation rather than relying on remembered defaults.
Caveat: SameSite cookies reduce one class of cross-site request risk but are not a complete defense by themselves.

Tags: bot-and-agent-security, cookies, session-security, checkout, admin-access, cross-site-request-forgery
Source: Site Security (1).docx

---

## Prefer Explicit Code Over Clever Code in Store Systems
Use when: Reviewing or writing code that touches checkout, payments, authentication, refunds or customer data on your store.
- Adopt the source's stated preference: take boring, plain, repetitive, explicit code over 'magical' code — even though the clever version is more fun to write.
- Apply this especially to security-relevant paths: authentication, session handling, pricing and discount calculation, refund and payment logic.
- When a framework or library hides behavior behind convention or reflection, spell out the security-relevant behavior explicitly where practical, so a reviewer can see what actually happens.
- This is a tradeoff, not an absolute: a well-maintained framework's built-in auth is often safer than custom code. The claim is specifically that among things you write yourself, explicit beats magical.
Caveat: This is the source's stated opinion, not a measured rule. It should be weighed against using maintained, well-tested library implementations for security primitives.

Tags: bot-and-agent-security, code-review, secure-development, checkout, maintainability
Source: Site Security (1).docx

---

## Make Dangerous Code Look Dangerous
Use when: Naming and organizing internal APIs in your store platform — especially functions that move money, expose customer data or change account state.
- Give genuinely risky operations a scary, unmistakable name rather than a friendly one (a function that irreversibly deletes customer data or force-charges a card should sound like what it does).
- Document the danger properly: what the function assumes, what it can destroy, and what the caller must guarantee before calling it.
- Do not combine dangerous operations with benign ones in the same function or call path — the source explicitly warns against putting the two together, because callers then invoke risk without realizing it.
- Apply this when designing internal tooling and admin actions: an admin 'quick fix' endpoint that can silently issue refunds or export customer data should be clearly labeled and separately permissioned.
- This supports auditability: a reader skimming the code should be able to spot the dangerous operations from the names alone.
Caveat: Naming is a human safeguard, not a technical control — it does not prevent misuse by a caller that ignores the warning.

Tags: bot-and-agent-security, secure-development, code-review, admin-access, api-design
Source: Site Security (1).docx

---

## Adopt a Paranoid, Vigilant Security Mindset
Use when: Setting expectations and habits for whoever maintains your store's security posture over time — platform owner, in-house dev or agency.
- Treat the source's claim that 'you can never be too paranoid in security' as a cultural stance: assume something you depend on can fail or be attacked.
- Translate vigilance into concrete practice rather than anxiety: keep dependency inventories, watch security advisories for your platform and payment stack, and re-check assumptions after major upgrades.
- Assume inputs from customers, webhooks, third-party integrations and other systems are untrusted until validated — this is the practical expression of paranoia in an ecommerce stack.
- Keep a paranoid posture toward your own past decisions too: a control that was adequate a year ago may not be adequate after a replatform or new integration.
- Balance this against change management: constant churn in checkout and payment code carries its own risk, so schedule reviews rather than making unscheduled risky edits during peak trading.
Caveat: Paranoia is a mindset, not a checklist; the source offers no specific procedures or benchmarks behind this advice.
Caveat: Vigilance must be bounded — unbounded rewrites of working checkout code during peak season are themselves a risk.

Tags: bot-and-agent-security, security-culture, risk-management, maintainability, payment-security
Source: Site Security (1).docx

---

## Smaller Packages Have Enlarged Modern Dependency Trees
Use when: Assessing supply-chain and update risk for the libraries your storefront, checkout or integrations depend on.
- Recognize the structural change the source describes: package managers like npm and Rust's ecosystem allow a local dependency model, so conflicting versions can coexist in a folder rather than forcing global resolution.
- That freedom lets authors publish much smaller units of functionality, so a single dependency can pull in a very large tree of transitive packages.
- The source frames this as a security tradeoff: more code arrives from more places, so there are more parties and more maintainers in your dependency graph.
- For your store, maintain an inventory of direct and transitive dependencies in your storefront, checkout and integration code, and check where each package's code actually originates.
- When a dependency or advisory affects you, evaluate the whole path — a tiny package can be the entry point to a deep tree.
- The source does not claim smaller packages are good or bad, only that their proliferation is a major ecosystem shift with more parties involved.
Caveat: The source is describing an ecosystem trend from its own time; package manager behavior and ecosystem norms continue to change, so verify current tooling for your stack.
Caveat: Dependency count alone is not a risk score — provenance, maintainership and how deeply a package sits in your checkout matter more.

Tags: bot-and-agent-security, supply-chain, dependencies, npm, secure-development, open-source
Source: Site Security (1).docx

---

## Standardized Collaboration Platforms Accelerated Code Flow
Use when: Evaluating the risk of third-party code, templates, plugins or themes you pull into your store from public repositories.
- The source contrasts older open source — where each project ran its own process, mailing list, version control and access model — with today's standardized platforms where everything is on GitHub.
- The consequence it highlights is scale and velocity: code flies around constantly, more contributors participate, and the review and governance process that used to be project-specific is now often lightweight and uniform.
- Translate this to your store: before adding a theme, app, plugin or library from a public repository, check who actually maintains it, how active it is and whether contributions are reviewed.
- Prefer sources with a visible maintenance process you can inspect over repositories that only look popular.
- When vendoring third-party code into checkout or customer-data paths, treat the speed and openness of the ecosystem as the reason for extra scrutiny, not less.
Caveat: The source is describing the general open-source ecosystem shift, not prescribing a vetting checklist; the specific vetting criteria above are the ecommerce adaptation, not a result the source demonstrated.
Caveat: Platform interfaces and repository features change; verify current tooling when checking maintainership signals.

Tags: bot-and-agent-security, supply-chain, open-source, third-party-integrations, code-review, risk-management
Source: Site Security (1).docx