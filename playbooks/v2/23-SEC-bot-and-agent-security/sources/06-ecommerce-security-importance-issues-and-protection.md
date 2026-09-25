# E-Commerce Security: Importance, Issues & Protection Measures

source_id: 1CVdtLnDDQfVHxiFDsC0xlFqwKWCvYrnw  |  folder: 23-SEC-bot-and-agent-security  |  cards: 20  |  words: 2,208  |  type: article (vendor/education blog post)
credibility: Author not named. The piece reads as vendor content for Astra Security: it promotes the "Astra Firewall" and "Astra Malware Scanner" by name and describes their features in detail, while spending far less detail on non-Astra controls. Evidence is generic industry statistics (no citation given for most), one attributed opinion (Roger Grimes, 2018), and three images credited to NIST, Comodo and Medium (likely reused diagrams, not this author's own research). No client data, no case studies, no named store. Treat the conceptual framing (the four pillars, common issue categories) as reliable teaching content, and treat all specific vendor capability claims as marketing to verify, not as tested results.
date signals: Statistics are dated to 2018 (32.4% of attacks in 2018; Roger Grimes quote dated 2018). No platform version numbers given. The FAQ block at the end reads as a later addition (broader, undated phrasing), suggesting the page was updated after original publication but the core stats were not refreshed.

## 1. What this source is for

A beginner-level orientation to ecommerce security: what it means, why small stores are exposed, and a short list of baseline controls (encryption, layered defense, firewalls, anti-malware, PCI DSS). It is useful as a plain-English framework (the four pillars) and as a checklist starting point, not as an implementation guide. It gives almost no step-by-step "how," and its named vendor is a product pitch, not a comparison.

## 2. Principles

1. **Privacy**: no one but the seller the customer chose should access that customer's personal and payment data. A breach of confidentiality happens when sellers let others access it. Minimum stack: anti-virus, firewall, encryption and other data protection. [e9fc52a7717a]
2. **Integrity**: customer-submitted data must stay as given, unaltered, in transit and storage. Any alteration erodes buyer confidence in the business. [86d4b5ae6b15]
3. **Authentication**: both buyer and seller must be provably real. Standard solutions named: client login credentials and credit card PINs; also MFA, magic links. If you cannot implement this yourself, the source says hire an expert. [66e6ee00a6cb]
4. **Non-repudiation**: neither party can deny a signature, email or purchase once it happened; this compensates for ecommerce having no live video/in-person confirmation. [5e4b42b4a48a]
5. **Use the four pillars as an audit lens**, not a certification: assign an owner to each pillar and review quarterly, since the source's condition is that gaps usually appear at new touchpoints (subscriptions, B2B portals, new payment methods) rather than at the original checkout. Meeting the four pillars does not equal PCI DSS compliance. [a1aa08fcea08]
6. **Security is continuous, not a one-time setup.** The source's closing position: don't stop at basic authentication, SSL and MFA, because attackers keep improving. [81d28e4a2a57]
7. **Frame security as a survival issue, not an IT line item**, when justifying budget: the source's evidence for this is the "almost 60% of small stores don't survive 6 months after a cybercrime incident" statistic (dated framing, see section 4). [ef80940bbfac]

## 3. Procedures

The source is thin on sequenced "how." It lists measures, not ordered workflows. The only concrete sequence given is for malware scanning:

1. Install anti-malware software that scans the web system and connected devices.
2. Turn on the "Schedule a Scan" feature and choose a cadence: daily, weekly, monthly or fortnightly. [verify UI: Astra Scanner interface, if this vendor is actually adopted]
3. Turn on file-change notifications so any modification triggers an alert.
4. On any detection, treat it as a breach until proven otherwise. [2abf4fa5b32e]

No other section of the source gives an ordered build sequence (not for SSL setup, not for WAF configuration, not for PCI DSS work, not for Shopify Flow). Where this playbook's cards describe a fuller procedure (order-risk automation, checkout-script inventory, layered defense build order), that detail was reasoned by the card writer from the principle, not copied from explicit source steps. Treat those as good practice extrapolated from a thin source, and verify independently.

## 4. Rules, thresholds and numbers

| Rule / statistic | Number | Condition | Source's basis | Card id |
|---|---|---|---|---|
| Share of all successful cyberattacks that hit online businesses | 32.4% | Stated for 2018 | Unattributed statistic in the source | ef80940bbfac |
| Consumers who made an online purchase in the last month | 85.6% | No year given | Unattributed statistic | ef80940bbfac |
| Small ecommerce owners who say attacks are getting worse | 50% | No year given | Unattributed statistic | ef80940bbfac |
| Share of website traffic that is malicious requests | 29% | No year given | Unattributed statistic | ef80940bbfac |
| Small ecommerce stores that don't survive 6 months after a cybercrime incident | ~60% | No year given | Unattributed statistic; correlation, not shown as causal | ef80940bbfac |
| Companies with MFA that are still successfully hacked | "most" (no percent given) | 2018 | Attributed quote: Roger Grimes, 2018 | 6c4dfeee0125 |
| Malware scan cadence options | daily / weekly / monthly / fortnightly | Astra Scanner feature, named vendor | Vendor feature description [web check: Astra Security] | 2abf4fa5b32e |
| WAF platforms with distinct configs named | WordPress, Magento, Opencart, Prestashop, Drupal, Joomla, custom PHP | Choosing a WAF for a self-hosted or plugin-based store | Vendor's supported-platform list [web check: Astra Security] | 965af11e3df4 |
| PCI DSS applicability | applies to "all businesses that handle credit card transactions" | Baseline claim, no version or requirement number given | Source's own general statement; verify against PCI SSC | 3c5e4e35f931 |

All 2018-dated figures should be treated as illustrative framing from the source, not current benchmarks. The source gives no thresholds for what counts as "high" malicious traffic, no chargeback-rate benchmark, and no capacity numbers for DDoS mitigation.

## 5. Diagnostics and checks

- **Missing SSL/TLS**: if a customer-facing page (including checkout, account, subdomains) is served over plain HTTP, treat all data on it as exposed to any device sitting between buyer and server; the fix is to install/renew a certificate and force HTTPS site-wide. [df34d29eeda1]
- **Unexplained record changes**: if a shipping address, order content or contact detail changes without a logged, deliberate action, treat it as a possible compromise signal, not a data-entry issue. [86d4b5ae6b15]
- **File-change alerts firing**: the source's stated signature of a malware injection is an unexpected file change; on any alert, rotate admin and integration credentials, check for new/unauthorized admin users or changed payment routes, and review checkout code. [2abf4fa5b32e]
- **Checkout script inventory**: list every script/app running on checkout and payment pages (analytics, chat, A/B test, tag manager); anything not required at the payment step is a skimming risk to remove. [00fe8dc22000]
- **WAF/firewall rule changes**: after any rule change, retest real login, checkout and webhook traffic end to end; a false positive here is a lost order, not just noise. [6c4dfeee0125], [965af11e3df4]
- **Example detection given**: "WP-VCD malware flagged by Astra's Malware Scanner" is referenced as a screenshot/example in the source, with no technical detail on how detection worked. Treat as illustration only. [2abf4fa5b32e]

## 6. Tools, settings and named features

- **CDN** (unnamed, generic): described as blocking DDoS and "infectious" traffic before it reaches the origin server, using machine learning. No vendor named for this claim. [web check: verify this claim against your actual CDN provider's documentation]
- **Multi-Factor Authentication / two-factor authentication**: generic description (login, then SMS or email step). No vendor named.
- **SSL/TLS certificates**: generic description of encrypting data across hops. Image credited to Comodo (a certificate authority) but no Comodo product is recommended in text.
- **Astra Firewall** (named vendor product): claimed to stop spam, XSS, CSRF, malware, SQLi and "100+ types of attacks"; claimed to have specialized WAF builds for WordPress, Magento, Opencart, Prestashop, Drupal, Joomla and custom PHP sites; claimed to block OWASP top 10 threats and bad bots. [web check: Astra Security's current firewall product and claims — this is vendor marketing copy in the source]
- **Astra Malware Scanner** (named vendor product): claimed unlimited scans, file-change notifications, ML-powered scanning, "collective intelligence," and cleanup of "credit card hack," Japanese spam, pub2srv, Pharma attacks and malicious redirects; has a "Schedule a Scan" feature (daily/weekly/monthly/fortnightly). [web check: Astra Security's current scanner product and claims] [verify UI: Schedule a Scan feature location, if adopted]
- **PCI-DSS** (standard, not a tool): referenced only as "comply with requirements," with a requirements image credited to Medium. No specific requirement numbers are given in the source body. [web check: current PCI DSS version and requirements via the PCI Security Standards Council]
- **NIST**: credited only as the source of an image illustrating the multi-layer/CDN concept; not otherwise discussed.
- **Shopify Flow and the shared-responsibility model on hosted platforms**: named only in this folder's scope note (the curator's framing of what belongs in this topic), not in the source's own body text. The source body never mentions Shopify, Shopify Flow, 3D Secure, AVS or CVV. Any playbook guidance on these (order-risk automation via Shopify Flow, 3DS/AVS/CVV checkout verification) is reasoned from the topic area, not drawn from this document. [web check: Shopify Flow's current capabilities, if used] — do not attribute this detail to this source.

## 7. Examples and case results

- **Roger Grimes, 2018** (quoted, unattributed to a specific publication): "Most companies that use MFA are still successfully hacked." Presented as an opinion/observation, not a study result. Use as a caution against over-trusting MFA, not as a statistic. [6c4dfeee0125]
- **WP-VCD malware flagged by Astra's Malware Scanner**: referenced as an image/example in the source with no further detail (what WP-VCD does, how it was found, remediation steps). Treat as a marketing screenshot, not a documented case. [2abf4fa5b32e]
- No other named case, brand or dollar-figure result appears in the source.

## 8. Mistakes the source warns about

- Treating MFA as a guarantee: most MFA-protected companies are still hacked (Roger Grimes, 2018). MFA is a layer, not a stop. [6c4dfeee0125]
- Skipping SSL/TLS on any customer-facing page: leaves passwords, usernames and card numbers readable to any intermediary device. [df34d29eeda1]
- Letting apps, staff or agencies keep customer-data access after they no longer need it (a "common confidentiality gap" per the source's framing). [e9fc52a7717a]
- Auto-correcting or silently altering customer-submitted data instead of flagging discrepancies — this is what breaks the integrity principle. [86d4b5ae6b15]
- Disclosing a support contact point for transparency but not disclosing how personal data is collected and used — the source calls this out explicitly as a gap in "improved transparency" efforts. [d8a54a766, 5e4b42b4a4]
- Ignoring counterfeit/lookalike sites and content tampering as a "someone else's problem" rather than a brand-protection task. [f7fc93724150]
- Running without a tested, ransomware-protected backup, so a worm/virus/defacement event has no fast recovery path. [994f398eea3e], [f7fc93724150]
- Treating a security review as a one-time setup instead of a recurring, owned cadence. [81d28e4a2a57]

## 9. Caveats, conflicts and what is missing

- **Vendor bias**: the two most detailed "protection measures" (Astra Firewall, Astra Malware Scanner) are also the two named commercial products in the piece. Per this playbook's own scope note, these product plugs should be treated as illustrations of a tactic (WAF, anti-malware scanning), not endorsements or comparisons against alternatives.
- **Stale statistics**: all headline numbers (32.4%, 85.6%, 50%, 29%, ~60%) are unattributed and dated around 2018 by the one attributed quote nearby. Do not present these as current benchmarks. [needs web check: current ecommerce cyberattack/breach statistics if this business case is being made today]
- **Shared-responsibility, Shopify Flow, 3DS, AVS, CVV are named in this folder's scope note but not covered by this source's own body text.** Do not cite this document as the source for those specifics; another document in this folder (04-how-to-make-your-shopify-store-more-secure.md) is the more likely fit for Shopify-specific claims.
- **One piece of source advice is explicitly out of scope for defensive guidance**: the source suggests embedding Google reviews on the site "for transparency" to reduce buyer uncertainty. That is a trust/marketing tactic, not a security control, and this playbook excludes it. [d8a54a7666e1]
- **No conflict with other sources is visible from this document alone** since no other source is cross-referenced here; check the folder-level Pass 2 playbook for whether other sources in 23-SEC disagree on MFA effectiveness, WAF choice or PCI DSS scope.
- **Depth gap**: the source gives no configuration detail anywhere — not for SSL setup, WAF rules, PCI DSS requirement checklist, or backup/ransomware tooling. It is a "what and why," not a "how."

## 10. Card index

- [a1aa08fcea08] Four pillars of ecommerce security mapped to store controls
- [6c4dfeee0125] Layered defense: block malicious traffic before it reaches origin
- [df34d29eeda1] SSL/TLS: encrypt data in transit across every hop
- [3c5e4e35f931] PCI DSS scope: who owns what across hosted vs self-hosted
- [f7fc93724150] Protect against counterfeit sites and brand abuse
- [d8a54a7666e1] Handle the fraud, dispute and delivery moment of uncertainty
- [2abf4fa5b32e] Anti-malware scanning and scheduled detection for storefront files
- [00fe8dc22000] Defend against digital skimming and payment-page tampering
- [965af11e3df4] Bot, spam and OWASP-class application defense with a WAF
- [66e6ee00a6cb] Layer passwords, PINs and magic links for buyer authentication
- [5e4b42b4a4] Non-repudiation: keep evidence that orders and consents happened
- [ef80940bbfac] Treat security failures as a survival risk, not an IT line item
- [994f398eea3e] Harden store networks against worms, Trojans and destructive payloads
- [893cc2b3b57c] Route traffic through selective-permeability firewalls
- [4156d47e2c2b] Automate high-risk order handling on hosted platforms
- [8a7af1a2b145] Map payment-fraud controls: verification checks at checkout
- [06bc968f35c3] Defend against denial-of-service and keep the store selling
- [86d4b5ae6b15] Integrity: keep customer data unaltered to preserve trust
- [e9fc52a7717a] Privacy: prevent unauthorized access to customer data
- [81d28e4a2a57] Run a continuous security review across store surfaces
