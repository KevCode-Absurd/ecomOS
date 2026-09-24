# Ecommerce Security: Threats and Best Practices

source_id: 1t4ZeEnClZTVulo6dPKtVZGhfSDvJHdrb  |  folder: /23-SEC-bot-and-agent-security  |  cards: 19  |  words: 3838  |  type: article (vendor blog post, Shopify)
credibility: This is a Shopify blog post (url: https://www.shopify.com/blog/ecommerce-security, rights: public_reference). Shopify sells the products it describes as solutions: Shopify Payments, Shopify Flow, Shopify Protect, Shopify Sidekick, automated privacy-policy templates, and the Customer Privacy API. Evidence mixes three kinds: (1) third-party research the source cites but did not produce — Juniper Research (fraud loss projections), IBM's 2025 Cost of a Data Breach Report, the 2025 Imperva Bad Bot Report, Sift's Q3 2025 Digital Trust Index, Usercentrics' State of Digital Trust in 2025; (2) Shopify's own product claims (PCI DSS compliance by default, free TLS certificates, fraud-analysis scoring, SOC audit cadence); (3) named-merchant case examples and quotes (Maine Lobster Now, Winter Park Cycles, Profumerie Griffe, Maggy London) that read as customer-marketing stories, not controlled studies. `[web check: verify current figures and product terms directly with Shopify and the cited research firms before citing them to a client]`
date signals: Modified 2026-09-20. Cites 2025 reports throughout (IBM 2025, Imperva 2025, Sift Q3 2025, Usercentrics 2025). States "As of June 2026, 98% of US web traffic on Google's platforms runs over HTTPS," which dates the HTTPS-adoption claim specifically. Projects chargeback volume toward 2029 ($46.1 billion) and fraud losses toward 2030 ($131 billion) and cites a $362 billion fraud-loss projection for 2023-2028. Treat all forward-looking figures as projections made at time of writing, not outcomes.

## 1. What this source is for

It gives a store owner a map of ecommerce-specific threats (payment fraud and card testing, account takeover, phishing, bot attacks, DDoS, data breaches, digital skimming), explains the shared-responsibility split between a hosted platform and the merchant, and lists concrete defensive configuration steps (2FA, AVS/CVV/3DS settings, Shopify Flow risk automation, app-permission audits, PCI DSS scope). It is strong on hosted-platform (Shopify) specifics and weak on self-hosted specifics: self-hosted guidance stays at the level of "you must do this yourself" without naming tools, vendors or steps. It is also a promotional piece for Shopify's own paid and built-in security features, so read every product claim as a vendor claim.

## 2. Principles

### 2.1 Shared responsibility model

1. **On a hosted platform, security is a two-way split, not a platform-only guarantee.** The platform secures infrastructure, servers, payment processing systems, checkout code and the software everything runs on. The store owner secures login credentials, third-party app permissions, sensitive customer-data handling, and who on the team has admin access. Neither side can compensate for the other's failure: the source's example is that Shopify cannot protect a store whose admin password is "password123" or whose owner clicks a phishing link, just as a store owner cannot patch servers that belong to the platform. [107b392be14e]
2. **On self-hosted setups, the merchant owns everything the platform would otherwise do.** That means sourcing and renewing SSL/TLS certificates, achieving PCI compliance independently, patching server software, and configuring firewalls, as ongoing technical work rather than one-time setup. [107b392be14e] [4458c67f9169]
3. **Prioritize merchant-side gaps first, since they are the side of the split you fully control.** The source's own ordering: enable 2FA and passkeys on admin accounts, audit app permissions, and stop storing card data in order notes, emails or spreadsheets. [107b392be14e]
4. **Hosted checkout code is not merchant-editable, which structurally reduces (not eliminates) skimming exposure.** Because merchants cannot alter the underlying checkout JavaScript on a hosted platform, digital-skimming (Magecart) attacks that inject malicious code into checkout pages are significantly less likely to succeed there than on a self-hosted store. [107b392be14e] [12d80d9aebc1]

### 2.2 The threat landscape

5. **Card-not-present (CNP) fraud runs through a specific attack chain: breach or phishing, then card testing, then resale or larger fraud.** Fraudsters obtain card data through data breaches, phishing attacks or skimming devices, then run small transactions to validate stolen numbers before using them for larger fraud or selling the validated data on dark web markets. Unusual clusters of small orders, especially from new accounts, mismatched geographies, or repeated attempts on the same card range, are the card-testing signal. [044017a04e87]
6. **Account takeover (ATO) is fed by credential stuffing and phishing, and both scale automatically.** Large-scale data breaches expose username/password pairs; attackers test those pairs systematically across other sites (credential stuffing) or use breached data to support more targeted phishing. Phishing itself is fake email, text or voice communication that impersonates a trusted source to extract login credentials or card details. [b64e851eb9f3]
7. **Bots operate at machine speed against APIs, not just the storefront front end.** Bots run card-testing attacks, scrape pricing data, create fake accounts and stockpile high-demand products before real shoppers can buy. The source cites the 2025 Imperva Bad Bot Report finding that 44% of advanced bot traffic now targets API endpoints, which handle checkout, inventory and customer account data. [07cc5eccc349]
8. **DDoS is a distributed traffic flood aimed at locking out real customers**, distinct from bot scraping or card testing; the source does not prescribe a specific mitigation stack for it beyond relying on platform-level protections. [07cc5eccc349]
9. **Digital skimming (Magecart) captures card data as the customer types it, inside the checkout page itself.** Skimming malware injects malicious JavaScript into a checkout page; the source calls these "brute force attacks" that target JavaScript and are hard to spot without regular code audits. HTTPS encryption in transit does not stop this, because the data is captured before or as it is typed, not intercepted over the wire. [12d80d9aebc1]

### 2.3 The cost of security failures

10. **A single security incident can trigger a chargeback bill, a regulatory fine and customer attrition at the same time.** The source frames these as compounding, not alternative, costs of one incident. [4d53cd87f3f6] [4a75dffc1efe]
11. **Processors watch chargeback rate as a hard operating limit, not a soft guideline.** Most processors flag accounts above a 0.9% chargeback rate; above 1%, processors can stop accepting cards completely. Card [9f8a9054c7e7] adds an important correction on top of the source's numbers: treat 0.9%/1% as illustrative, and get the current monitoring definitions, thresholds, periods and denominator directly from your own processor or acquirer, since programs count disputes and transactions differently.
12. **GDPR applies by customer location, not store location, and the penalty ceiling is severe.** If a store sells to customers in the EU or UK, GDPR applies regardless of where the store is based. Serious violations carry fines up to 4% of a company's global annual revenue, on top of breach costs and possible customer compensation claims. [4d53cd87f3f6]
13. **Security failures measurably reduce trust and future spend, and the effect spreads to other customers.** The source cites Sift's Q3 2025 Digital Trust Index finding that 75% of consumers say they would stop using a site after an account takeover there, and 87% would share the experience with others. [b64e851eb9f3] [4a75dffc1efe]
14. **Missing HTTPS is now a visible, conversion-relevant warning, not a background technical detail.** Modern browsers flag any site without HTTPS with a "Not secure" warning in the address bar, visible at the exact moment a customer decides whether to enter card details. [4a75dffc1efe]
15. **Privacy transparency independently affects retention.** The source cites Usercentrics' State of Digital Trust in 2025 finding that 36% of consumers have stopped using a website due to privacy concerns, separate from any breach. [4d53cd87f3f6]

### 2.4 Platform defaults and vendor features (Shopify-specific; vendor claims)

16. **Every Shopify store is PCI DSS-compliant by default, and gets a free TLS certificate with HTTPS on by default.** [Shopify vendor claim] Managing PCI DSS independently instead means annual self-assessments, quarterly vulnerability scans, and potentially a paid audit by a Qualified Security Assessor (QSA). All Shopify card readers are stated to be PCI and EMV (Europay, Mastercard, Visa) compliant. [4458c67f9169]
17. **Shopify's fraud analysis scores every order using multiple signals and assigns a low/medium/high risk rating.** [Shopify vendor claim] Signals used: AVS checks, CVV verification, IP address data, proxy detection, and unusual purchase patterns. [b7ac80d4a328] [4458c67f9169]
18. **Shopify Protect (formerly Fraud Protect) is a guaranteed chargeback-coverage program, not a universal guarantee.** [Shopify vendor claim] It is available to eligible Shopify Payments users in the US only. On orders Shopify marks as protected, payment is guaranteed, and if a dispute is filed, Shopify covers the chargeback and the dispute fee. Eligibility and geography must be checked in current platform documentation before you rely on it. [269345a2fe3f]
19. **Shopify Sidekick is cited as an early bot-detection example, not a documented detection standard.** [Shopify vendor claim, single case] It flagged a major bot attack on Maggy London's storefront before any other monitoring system, per the source. Treat this as one illustrative case, not a benchmark for detection performance. [07cc5eccc349] [7e755c997f22]

### 2.5 Store-owner best practices

20. **Two-step authentication (2FA) is mandatory for Shopify Payments and should be treated as mandatory for every admin account, not only payment-related ones.** Shopify also supports passkeys as an additional authentication layer. [b64e851eb9f3] [397cd5d09b61]
21. **Fraud-prevention settings (AVS, CVV, mismatched-billing handling) need review before you change defaults, not after.** AVS is deactivated by default in Shopify Payments because fraud analysis already handles high-risk transactions separately; turning AVS on alongside fraud analysis can raise false declines on legitimate orders, so review order risk reports first. [284cbb2a9af0]
22. **Automate order-risk handling with rules, because card testing and fraud run faster than manual review.** Common configurations: auto-capture low-risk orders, add high-risk orders to a manual review queue, send internal notifications for medium-risk orders, and cancel orders matching specific fraud patterns. Keep a human escalation path on the medium- and high-risk queues so automated cancellation does not silently reject legitimate high-value customers. [b7ac80d4a328]
23. **Team training against phishing must now account for generative-AI-written attacks that pass basic grammar and formatting checks.** Training should cover identifying suspicious sender domains, verifying any request for credential changes or payment redirects through a separate channel, and how to report suspicious email (phishing), voice (vishing) and SMS (smishing) attempts. [b64e851eb9f3]
24. **Every installed app is part of your data-handling surface, regardless of how clean your own checkout is.** Apps can access order data, customer information or store settings depending on the permissions granted at install. Regularly review installed-app permissions and remove unused apps. When selecting new apps, prioritize "Built for Shopify" status and review scores above 3.75, since those apps are reviewed against Shopify's technical requirements. A badge or score is a heuristic, not a guarantee. [39c0311f77d5]
25. **Never let card data leave the compliant checkout channel.** Do not ask customers for card details outside checkout. Never store card numbers in order notes, emails, spreadsheets or shared documents. If a customer sends card details by email or chat, treat that message as an exposure event, do not process it manually, and redirect the customer to the compliant checkout flow. Apply the same rule to app and integration data flows. [0beedce68579]

### 2.6 Payment security specifics

26. **AVS, CVV and 3DS are three distinct controls that catch different failure modes; none is sufficient alone.** AVS checks whether the billing address matches the card issuer's records. CVV (the 3- or 4-digit card code) makes stolen card numbers harder to use without physical access but does not prove cardholder identity. 3DS adds a multifactor step (one-time code or biometric) for higher-risk transactions. Combine them and monitor outcomes rather than relying on any single one. [284cbb2a9af0]
27. **Dynamic 3D Secure can shift fraudulent-chargeback liability from the store to the card issuer.** When a cardholder completes 3DS verification, the source states responsibility for a fraudulent chargeback on that transaction moves to the issuer for authenticated Visa and Mastercard disputes. Only 32.4% of store owners currently implement 3DS, per the source. Treat 3DS as a liability-shift and verification tool, not proof the buyer is the genuine cardholder; monitor approval rates and false declines after enabling it. `[web check: current liability-shift rules by network, region and processor]` [72f778d69825]
28. **PCI DSS has 12 core requirements and applies to every business accepting card payments, regardless of size.** Requirements cover network security, encryption, access controls, monitoring and security policies. Most small ecommerce stores fall into Level 4 (fewer than 20,000 transactions per year), which the source says requires an annual self-assessment questionnaire (SAQ) rather than a formal third-party audit. Card [191971551b04] adds a needed correction: do not infer your required assessment from a universal 20,000-transaction rule; confirm the actual validation route and SAQ eligibility with your acquirer or payment brand, and map where payment data is actually captured, processed and stored across your store, apps and support workflows.
29. **On Shopify, platform-level PCI compliance does not cover merchant workflows outside the checkout.** Shopify processes and stores card data in a PCI DSS-compliant environment, but the merchant's residual responsibility is to avoid introducing non-compliant handling: not asking for card details outside checkout, never storing numbers in notes, emails or spreadsheets. [191971551b04] [0beedce68579]
30. **When choosing any payment gateway, verify three things before committing: processor-level PCI DSS certification, tokenization support, and 3DS 2.0 support.** Certification of your own storefront does not substitute for processor-side compliance. Check certifications directly with the provider rather than relying on marketing pages, and re-verify periodically since terms change. Shopify Payments is described (vendor claim) as PCI-compliant by default with built-in fraud analysis, 3D Secure and Shopify Protect for eligible stores; third-party gateways can be used but bring their own compliance and security requirements. [7850639e8e8f]

### 2.7 Trust signals

31. **Visible security signals belong at the specific moment a customer decides to enter payment details, not just anywhere on the site.** The padlock icon and HTTPS prefix are the most widely recognized signals. Shop Pay stores returning users' shipping and payment details securely, reducing checkout friction. Third-party trust badges can supplement these, particularly for security-conscious categories like health products or high-value goods. [4a75dffc1efe]
32. **Treat HTTPS as baseline hygiene, not a differentiator.** As of June 2026 (source's figure), 98% of US web traffic on Google's platforms already runs over HTTPS, making encryption an expectation rather than something that sets a store apart. [4a75dffc1efe]
33. **A clear, specific privacy policy is a trust and retention factor, not only a compliance checkbox.** GDPR requires clear disclosure of what data is collected, why, and how it is stored, for EU/UK customers. On Shopify, automated privacy-policy templates (vendor claim) cover core requirements, and the Customer Privacy API supports GDPR-standard cookie-consent banners. [4d53cd87f3f6]
34. **Independent third-party audits are a diligence signal for the platform, not for your store's own workflows.** The source states Shopify undergoes SOC 1 and SOC 2 audits every six months, verifying controls over customer-data encryption, access management, incident response and physical infrastructure. Treat these as covering the platform's environment only; your own apps, workflows and data handling are not covered by the platform's audit. [4d53cd87f3f6]

## 3. Procedures

The source gives named admin paths for 4 configuration tasks. All are marked `[verify UI]` since Shopify's admin navigation changes.

### 3.1 Enable two-step authentication (2FA)
1. Go to your profile in the Shopify admin.
2. Select **Manage account**.
3. Follow the two-step authentication setup under **Security**.
4. Add a passkey as an additional authentication layer where supported.
`[verify UI]` [b64e851eb9f3] [397cd5d09b61]

### 3.2 Configure fraud-prevention settings (AVS, CVV, mismatched billing)
1. Go to **Settings → Payments → Shopify Payments → Manage → Fraud prevention**.
2. Note that AVS is off by default because Shopify's fraud analysis already covers high-risk transactions separately.
3. Before turning AVS on, review your order risk reports, since enabling it alongside fraud analysis can raise false declines on legitimate orders.
4. Set CVV verification requirements and choose how checkout should handle a mismatched billing address.
`[verify UI]` [284cbb2a9af0]

### 3.3 Set up automated high-risk order handling with Shopify Flow
1. Go to **Apps → Shopify Flow**.
2. Select the relevant order-risk triggers (risk ratings come from Shopify's fraud analysis: low, medium, high).
3. Build workflows: auto-capture low-risk orders; add high-risk orders to a manual review queue; send internal notifications on medium-risk orders; cancel orders matching specific fraud patterns.
4. Start from a pre-built fraud workflow template in the Shopify Help Center library, then adapt thresholds to your store's order profile and risk tolerance.
5. Keep a human escalation path on medium- and high-risk queues; do not let cancellation rules run unreviewed.
6. Revisit the automation as order volume and fraud patterns change; a rule set tuned for one season can misfire later.
`[verify UI]` [b7ac80d4a328]

### 3.4 Audit installed apps and third-party integrations
1. Go to **Settings → Apps and sales channels**.
2. Review the permissions listed for each installed app (order data, customer information, store settings access).
3. Remove any app no longer in use.
4. For new apps, prioritize "Built for Shopify" status and a review score above 3.75.
5. Re-audit after adding any app with checkout, payment or customer-data access.
`[verify UI]` [39c0311f77d5]

### 3.5 Prioritization sequence when resources are limited (card's synthesis of the source's ordering)
1. Enable 2FA on every admin account; add passkeys where supported. Account protection gates everything else, since a weak or phishable admin credential defeats every other control. [397cd5d09b61]
2. Turn on the platform's built-in fraud analysis and wire its risk ratings into automated order handling (procedure 3.3). [397cd5d09b61]
3. Apply dynamic 3D Secure so higher-risk transactions get step-up authentication and chargeback liability can shift to the issuer; check eligibility for a guaranteed chargeback-coverage program. [397cd5d09b61]
4. Tighten AVS and CVV settings carefully, watching for false declines on legitimate customers before changing defaults (procedure 3.2). [397cd5d09b61]
5. Add organizational controls last, but do not skip them: phishing training, app-permission audits (procedure 3.4), and a hard rule against handling card data outside checkout. These address human and integration paths that technical controls miss. [397cd5d09b61]

## 4. Rules, thresholds and numbers

| rule | number or threshold | condition | source's basis | card id |
|---|---|---|---|---|
| Chargeback flag threshold | above 0.9% chargeback rate | processor review trigger | source's stated figure; card 9f8a9054c7e7 says confirm current definition with your own processor | 9f8a9054c7e7 |
| Chargeback hard limit | above 1% | processor can stop accepting cards completely | source's stated figure | 9f8a9054c7e7 |
| Average chargeback cost | about $128 per chargeback in fees and internal costs | per disputed transaction | source-cited figure | 397cd5d09b61 |
| Global chargeback value projection | $46.1 billion by 2029 | industry-wide | source-cited projection | 397cd5d09b61 |
| Cost per dollar of fraud lost | about $4.61 once processing fees, lost inventory and disruption are counted | CNP fraud | source-cited figure | 044017a04e87 |
| Global ecommerce fraud loss projection | $362 billion between 2023 and 2028 | industry-wide | Juniper Research, as cited (source itself flags this as a "skip" figure that doesn't change merchant configuration strategy) | 044017a04e87 |
| Global fraud loss projection (later figure) | expected to exceed $131 billion by 2030 | industry-wide | source-cited projection | none (FAQ text) |
| Phishing as breach cause | 16% of all breaches studied | initial-access vector | IBM 2025 Cost of a Data Breach Report, as cited | b64e851eb9f3 |
| Account takeover scale | affected 6 million consumers in 2025, up 18% from 2024; losses reaching $17 billion in 2025 | industry-wide | source-cited figures | b64e851eb9f3 |
| Bot traffic targeting APIs | 44% of advanced bot traffic | targets checkout, inventory and account APIs | 2025 Imperva Bad Bot Report, as cited | 07cc5eccc349 |
| Average data breach cost, global | $4.4 million in 2025 | per breach | source-cited figure | none (body text) |
| Average data breach cost, US | $10.22 million (record, highest in the world) | per breach, US businesses | source-cited figure | none (body text) |
| GDPR fine ceiling | up to 4% of global annual revenue | serious violations | source's stated rule | 4d53cd87f3f6 |
| GDPR fines issued | approximately €1.2 billion by EU/UK supervisory authorities in 2025 | industry-wide | source-cited figure | 4d53cd87f3f6 |
| Breach-notification rate | average 443 per day, up 22% year over year | EU/UK regulatory reporting | source-cited figure | 4d53cd87f3f6 |
| Consumer churn after ATO | 75% would stop using the site; 87% would share the experience with others | after an account-takeover incident | Sift Q3 2025 Digital Trust Index, as cited | b64e851eb9f3 / 4a75dffc1efe |
| Churn from privacy concerns | 36% of consumers have stopped using a website | due to privacy concerns generally | Usercentrics' State of Digital Trust in 2025, as cited | 4d53cd87f3f6 |
| HTTPS adoption | 98% of US web traffic on Google's platforms | as of June 2026 | source-cited figure | 4a75dffc1efe |
| 3DS adoption | only 32.4% of store owners currently implement 3DS | industry-wide | source-cited figure | 72f778d69825 |
| Self-hosted PCI cost | roughly $1,000 to $10,000 per year | depending on transaction volume | source-cited estimate | 107b392be14e |
| PCI DSS core requirements | 12 requirements | every business accepting card payments, any size | source's stated structure | 191971551b04 |
| PCI DSS Level 4 threshold | fewer than 20,000 transactions per year | qualifies for annual SAQ instead of formal third-party audit | source's stated rule; card 191971551b04 warns not to treat this as universal without confirming with your acquirer | 191971551b04 |
| App vendor quality heuristic | "Built for Shopify" status and review score above 3.75 | when selecting new apps | Shopify's stated review criteria | 39c0311f77d5 |
| SOC audit cadence | SOC 1 and SOC 2 audits every 6 months | Shopify's own platform environment, not merchant workflows | source-cited figure (vendor claim) | 4d53cd87f3f6 |
| Shopify Protect eligibility | eligible Shopify Payments users in the US only | guaranteed chargeback coverage program | source's stated scope (vendor claim, verify current terms) | 269345a2fe3f |

## 5. Diagnostics and checks

| check | how | good | bad | next step | card |
|---|---|---|---|---|---|
| Is the chargeback rate approaching the processor's danger zone? | Get current thresholds, periods and denominator from your own processor or acquirer; do not assume 0.9%/1% applies to your program `[needs brand data: processor chargeback reports]` | Rate well under the processor's flagged threshold | Rate near or above 0.9%, or already above 1% | Set internal alerts earlier than the processor's threshold; investigate fraud, delivery and customer-service causes; review authentication and evidence collection | 9f8a9054c7e7 |
| Are orders showing a card-testing pattern? | Watch for clusters of small transactions, especially from new accounts, mismatched geographies, or repeated attempts on the same card range `[needs brand data: order and decline logs]` | No unusual small-order clustering | Clusters of small test transactions | Tighten CVV/AVS review, escalate to processor fraud tools, treat as a signal not organic demand | 044017a04e87 |
| Is 3DS enabled and tuned? | Check checkout authentication settings and compare approval rates before/after enabling dynamic 3DS `[verify UI]` `[needs brand data: approval-rate and false-decline data]` | 3DS live on higher-risk transactions with stable approval rates | 3DS off entirely, or on and suppressing legitimate conversions | Enable dynamic 3DS; monitor false declines and adjust | 72f778d69825 |
| Is AVS creating false declines? | Enable AVS only after reviewing order risk reports; compare decline rate before/after `[verify UI]` `[needs brand data: order risk reports, decline rate]` | Low false-decline rate after enabling | Rising declines on legitimate-looking orders | Loosen AVS handling of mismatches or revert; rely on fraud analysis instead | 284cbb2a9af0 |
| Is 2FA enforced on every admin account? | Review admin user list and authentication settings `[verify UI]` | 2FA (and passkeys where possible) on all admin accounts | Any admin account without 2FA | Enforce 2FA per procedure 3.1 | b64e851eb9f3 / 397cd5d09b61 |
| Are installed apps over-permissioned or unused? | Review Settings → Apps and sales channels; check each app's granted permissions `[verify UI]` | Only active apps, with permissions matching their actual function | Unused apps still installed, or apps with broad order/customer-data access beyond their function | Remove unused apps; prefer "Built for Shopify" apps with review score above 3.75 | 39c0311f77d5 |
| Is card data leaking outside checkout? | Audit support, order-note and fulfillment channels for card numbers `[needs brand data: support ticket and order-note review]` | No card data found outside the checkout flow | Card numbers found in emails, chat logs, notes or spreadsheets | Redirect customers to compliant checkout; retrain staff; purge exposed data per policy | 0beedce68579 |
| Is your PCI scope actually confirmed, not assumed? | Ask your acquirer or payment brand which SAQ and validation route apply to your actual environment; map where payment data is captured, processed and stored, including apps and support | Confirmed SAQ level and scope from the acquirer | Assuming Level 4 / SAQ eligibility from the 20,000-transaction figure alone | Get the acquirer's determination in writing | 191971551b04 |
| Is your gateway (if not Shopify Payments) actually certified? | Check processor-level PCI DSS certification, tokenization support and 3DS 2.0 support directly with the provider `[web check: current provider certifications]` | Provider confirms all three in writing | Relying on marketing copy alone | Get written certification confirmation before committing | 7850639e8e8f |
| Does the store show visible trust signals at the payment moment? | Check for HTTPS/padlock, Shop Pay availability, and category-appropriate trust badges on checkout pages | Padlock and HTTPS present; trust badges used where the category warrants them | Missing HTTPS ("Not secure" warning shown), no trust signals near payment fields | Add TLS/HTTPS (platform-provided on Shopify); add trust badges for security-conscious categories | 4a75dffc1efe |
| Is the privacy policy specific and current for GDPR scope? | Confirm whether you sell to EU/UK customers; review privacy policy content against GDPR disclosure requirements `[needs brand data: EU/UK sales exposure]` | Clear disclosure of what is collected, why, and how it is stored | Generic or missing disclosure while selling into EU/UK | Update policy; confirm cookie-consent banner meets GDPR standards | 4d53cd87f3f6 |

## 6. Tools, settings and named features

- **Shopify Payments**: built-in payment processor; PCI-compliant by default (vendor claim); includes fraud analysis, dynamic 3D Secure and Shopify Protect eligibility. `[verify UI]`
- **Shopify Flow**: automation app used to route orders by fraud-analysis risk rating (auto-capture, manual review queue, notifications, auto-cancel). Free templates also cover abandoned carts, inventory alerts, customer emails and order routing (vendor claim). `[verify UI]`
- **Shopify Protect** (formerly Fraud Protect): guaranteed chargeback coverage and dispute-fee removal on eligible protected US orders. `[verify UI]` [269345a2fe3f]
- **Shopify Sidekick**: cited once as an early bot-detection tool in the Maggy London case (vendor claim, single example). [07cc5eccc349]
- **AVS (Address Verification System)**: checks billing address against the issuer's records. Off by default in Shopify Payments. `[verify UI]` [284cbb2a9af0]
- **CVV (Card Verification Value)**: 3- or 4-digit card code check. [284cbb2a9af0]
- **3D Secure (3DS), applied dynamically**: step-up authentication (one-time code or biometric) on higher-risk transactions; can shift chargeback liability to the issuer. Gateway selection should confirm 3DS 2.0 support specifically. [72f778d69825] [7850639e8e8f]
- **Tokenization**: replacing card data with a non-sensitive token; a gateway-selection requirement alongside PCI certification and 3DS 2.0. [7850639e8e8f]
- **PCI DSS SAQ (Self-Assessment Questionnaire)**: annual self-assessment for Level 4 merchants (under 20,000 transactions/year), instead of a formal third-party audit. [191971551b04]
- **QSA (Qualified Security Assessor)**: performs the formal third-party PCI audit merchants would otherwise need without a hosted platform. [4458c67f9169]
- **TLS/HTTPS**: free TLS certificate, HTTPS on by default on Shopify (vendor claim). [4a75dffc1efe]
- **Customer Privacy API**: supports GDPR-standard cookie-consent banners on Shopify (vendor claim). `[verify UI]` [4d53cd87f3f6]
- **Shop Pay**: stores returning customers' shipping/payment details securely; reduces checkout friction and functions as a trust signal. [4a75dffc1efe]
- **SOC 1 / SOC 2 audits**: independent audits of Shopify's own controls (encryption, access management, incident response, physical infrastructure), run every 6 months per the source (vendor claim); covers the platform's environment, not merchant workflows. [4d53cd87f3f6]
- **"Built for Shopify" badge / app review score**: heuristic for vetting third-party apps before install (threshold: score above 3.75). `[verify UI]` [39c0311f77d5]

## 7. Examples and case results

All are named-merchant or single-case examples cited by a vendor blog, not controlled studies. Treat every number below as an example, not a guarantee.

- **Maine Lobster Now**: chargeback rate was 0.25% of total transactions before switching to Shopify Payments with integrated fraud management. After switching, chargebacks due to fraud fell to 0.025%, a stated 93% reduction. Owner quote (Julian Klenda, CEO): fraud handling used to be almost a full-time role for one staff member; after the switch, that time was redirected to customer experience. [269345a2fe3f]
- **Winter Park Cycles**: after switching to Shopify, recorded $600,000 in sales with zero chargebacks across around 1,000 orders in the first 90 days. Owner quote (Ward Bates): "We haven't had one chargeback out of 700 orders in the past two months... Shopify's fraud notification system does a much better job screening ahead of time." [4458c67f9169] [b7ac80d4a328]
- **Profumerie Griffe**: quote from Alessandro Labozzetta (ecommerce project manager) crediting Shopify's Fraud Control with preventing fraudulent transactions and reducing transaction costs and checkout friction. [269345a2fe3f]
- **Maggy London**: Shopify Sidekick flagged a major bot attack on this storefront before any other monitoring system, per the source. Single-case illustration, not a benchmark. [07cc5eccc349] [7e755c997f22]
- **Signal-quality worked example (from the CNP fraud discussion elsewhere in the library, referenced here for the cost framing)**: each dollar lost to fraud costs store owners an average of about $4.61 once processing fees, lost inventory and operational disruption are counted. [044017a04e87]

## 8. Mistakes the source warns about

1. Assuming platform-level security (PCI, TLS, fraud scoring) covers merchant-side gaps like weak admin passwords or phishing susceptibility. [107b392be14e]
2. Skipping self-hosted responsibilities (certificate renewal, PCI compliance, patching, firewalls) because "the platform handles security." [107b392be14e]
3. Treating a padlock icon or HTTPS as protection against digital skimming; skimming captures data as it is typed, inside a page that may still be encrypted in transit. [12d80d9aebc1]
4. Reviewing every order manually instead of configuring automated fraud-risk workflows; card testing and bot activity run at machine speed. [044017a04e87] [b7ac80d4a328]
5. Enabling AVS without first reviewing order risk reports, which can spike false declines on legitimate orders. [284cbb2a9af0]
6. Treating AVS, CVV or 3DS as individually sufficient; each catches a different failure mode and each can be defeated or cause false declines. [284cbb2a9af0]
7. Assuming a universal 20,000-transaction rule determines your PCI SAQ eligibility without confirming with your acquirer or payment brand. [191971551b04]
8. Relying on a payment gateway's marketing page instead of verifying PCI certification, tokenization and 3DS 2.0 support directly with the provider. [7850639e8e8f]
9. Letting automated cancellation rules run on high-risk orders with no human escalation path, risking silent rejection of legitimate high-value customers. [b7ac80d4a328]
10. Not training staff against generative-AI-crafted phishing, which now passes basic grammar and formatting checks. [b64e851eb9f3]
11. Leaving unused apps installed, or installing apps without reviewing their data-access permissions. [39c0311f77d5]
12. Asking customers for card details outside checkout, or storing card numbers in order notes, emails or spreadsheets. [0beedce68579]
13. Treating trust badges or privacy copy as a substitute for actual controls; false or outdated signals can worsen trust. [4a75dffc1efe]
14. Assuming a platform's third-party audit (SOC 1/SOC 2) covers your own store's apps, workflows or data handling. [4d53cd87f3f6]
15. Assuming any single control or fixed sequence guarantees protection; each control reduces a specific risk, and several (AVS, 3DS) can also increase false declines. [397cd5d09b61]

## 9. Caveats, conflicts and what is missing

- **Vendor source promoting its own paid and built-in features.** This is a Shopify blog post. Every claim about Shopify Payments, Shopify Flow, Shopify Protect, Shopify Sidekick, default PCI compliance, TLS certificates, and SOC audit cadence is a vendor claim about Shopify's own product. The merchant case studies (Maine Lobster Now, Winter Park Cycles, Profumerie Griffe) are customer-marketing quotes, not independent or controlled evidence. `[web check: verify current Shopify product terms, eligibility and feature availability directly]`
- **The source itself flags some of its own cited statistics as not actionable.** Its own scope notes say to skip "broad global fraud damage estimates (e.g., $362 billion between 2023 and 2028) that do not change merchant configuration strategy," yet the body text includes this figure along with several other broad industry projections ($131 billion by 2030, $46.1 billion in chargebacks by 2029, €1.2 billion in GDPR fines). Use these for context only, not as planning inputs for a specific store.
- **Tension between the source's stated PCI Level 4 rule and the card-level correction.** The source states the 20,000-transaction-per-year threshold for Level 4 SAQ eligibility as if it were a fixed, universal rule. Card [191971551b04] correctly warns against inferring the required assessment from that number alone and instead directs the reader to confirm scope and validation route with the acquirer or payment brand. Treat the card's caution as the safer operating rule.
- **Self-hosted guidance is thin.** Beyond naming the categories of work (SSL/TLS, PCI compliance, patching, firewalls, cost estimate of $1,000-$10,000/year), the source gives no self-hosted-specific tools, vendors, or step-by-step configuration. It is written from a hosted-platform (Shopify) perspective throughout.
- **No WAF (web application firewall) or backup/disaster-recovery guidance is given.** The source names "firewalls" once, generically, for self-hosted setups, but does not name a WAF product, a backup cadence, or a disaster-recovery procedure anywhere in the text. Do not assume these are covered; they would need a separate source.
- **DDoS mitigation has no named stack.** The source defines DDoS and states hosted platforms provide some protection, but names no specific mitigation vendor, service or configuration step.
- **Liability-shift rules for 3DS are stated as general Visa/Mastercard behavior, not verified against current network or regional rules.** `[web check: current 3DS liability-shift rules by card network, region and processor]`
- **Chargeback thresholds (0.9%/1%) are presented as if fixed across all processors.** Card [9f8a9054c7e7] is the more defensible position: get current definitions, thresholds and denominators from your own processor, since programs vary.
- **No conflict found with common ecommerce security advice** (2FA, PCI compliance, AVS/CVV/3DS, HTTPS, app-permission audits, and not storing card data outside checkout are all standard, widely-taught practices). The one point worth flagging to a store owner used to generic advice: this source frames AVS as something to leave off by default on Shopify Payments specifically, because Shopify's separate fraud-analysis layer already covers high-risk transactions; a store owner coming from generic PCI guidance might assume AVS should always be on, and the source explicitly warns that doing so can raise false declines.

## 10. Card index

- 107b392be14e  Shared responsibility model: what the platform secures vs. what you secure
- 044017a04e87  CNP fraud and card testing: the mechanism to defend against
- 9f8a9054c7e7  Chargeback thresholds: know your danger zone
- 72f778d69825  Dynamic 3D Secure and the liability shift
- b7ac80d4a328  Automated order risk handling with workflow tools
- 284cbb2a9af0  AVS, CVV and 3DS: keep the three verification tools distinct
- 191971551b04  Confirm merchant PCI scope with the acquirer and payment setup
- 7850639e8e8f  Payment gateway selection: what to verify before committing
- b64e851eb9f3  Account takeover, credential stuffing and phishing defenses
- 39c0311f77d5  Auditing third-party apps and integrations
- 12d80d9aebc1  Digital skimming (Magecart): why hosted checkout reduces exposure
- 07cc5eccc349  Bot attacks, API targeting and DDoS: what to watch
- 4a75dffc1efe  Security failures as retention and conversion risk
- 4d53cd87f3f6  Privacy policy, GDPR exposure and third-party audit signals
- 269345a2fe3f  Guaranteed chargeback coverage programs: eligibility and limits
- 0beedce68579  Preventing card data from leaking outside checkout
- 397cd5d09b61  Prioritizing fraud controls when resources are limited
- 4458c67f9169  Assessing platform-level security defaults before you rely on them
- 7e755c997f22  Bot and fraud monitoring for inventory and high-demand drops
