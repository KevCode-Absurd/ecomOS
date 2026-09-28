# Security: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | done |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | done |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | done |
| 0.4 | `audit.py`: 22 rules in the contract shape, one or more per room job | done |

## JTBD table (room "Security", agent MONEY) and the audit rules that answer it

| Job | Question | Capabilities | Rules (audit.py) | Round 0 state on Bombas |
|---|---|---|---|---|
| Bot and AI-agent traffic policy | what is hitting our site that is not a person | MONEY-C41 | SEC-R07 bot share, SEC-R08 agent endpoint, SEC-R09 form captcha | R07 unavailable (edge bot analytics); R08 fires (UCP/MCP endpoint to review); R09 passes (hCaptcha) |
| Fraud and abuse across checkout, cards, returns | card testing, false declines, return abuse | MONEY-C42, MONEY-C76 | SEC-R01 chargeback lines, SEC-R02 win rate, SEC-R03 card testing, SEC-R04 promo abuse, SEC-R05 return abuse | R01 passes (0.08 percent, under 0.15); R02 passes this window; R03 to R05 unavailable |
| Account takeover, correlated across systems | could someone take over an account | MONEY-C43, MONEY-C81 | SEC-R06 | unavailable (platform admin logs) |
| Web application defects | exploitable defect in storefront or checkout | MONEY-C44 | SEC-R10 | unavailable (weekly scanner) |
| Third-party scripts, apps, dependencies | which apps and scripts are risky | SITE-C13 | SEC-R11 script count, SEC-R12 unknown hosts | R11 fires (7 over 5, tag manager); R12 unavailable (speed_runs keeps totals only) |
| Admin access and least privilege | only the access they need | MONEY-C46 | SEC-R13 | unavailable (Shopify staff list) |
| Backups and incident runbook | can we recover | MONEY-C47 | SEC-R14 | unavailable (backup export) |
| Domain, DNS, impersonation | is our domain safe | MONEY-C48 | SEC-R15 | unavailable (DNS audit, domain watch) |
| Privacy, consent, tracking | GDPR/CCPA and consent exposure | MONEY-C49 | SEC-R16 consent, SEC-R17 policy age | both pass (OneTrust; policy effective 2026-04-09) |
| Quarterly audit and PCI scope | four pillars, which SAQ | MONEY-C50, MONEY-C74 | SEC-R18 | unavailable (manual assessment) |
| Email authentication | can someone spoof our domain | MONEY-C72 | SEC-R19 | unavailable (DNS lookup) |
| Keys and credentials | which keys are overdue | MONEY-C73 | SEC-R20 | unavailable (secrets export) |
| Staff phishing training | would staff catch a phish | MONEY-C75 | SEC-R21 | unavailable (training platform) |
| Vendor risk | did the vendor pass a check first | MONEY-C77 | SEC-R22 | unavailable (vendor register) |

Round 1 candidates from this table: return abuse per customer from `orders` joined to `reversed_orders` (a real signal without the receiving log), dispute evidence packets for open disputes, a scripts-on-checkout check once the speed lab keeps request hosts, a MONEY-C81 cross-system login view once any admin log connects.

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- what is hitting our site that is not a person, and what should happen to it  (MONEY-C41)
- are we losing money to card testing, false declines or return abuse  (MONEY-C42, MONEY-C76)
- could someone take over an account, and would we see it across every connected system  (MONEY-C43, MONEY-C81)
- does our storefront or checkout code have an exploitable defect  (MONEY-C44)
- what apps and scripts have access to our store, and are any of them risky  (SITE-C13)
- does every staff member have only the access they need, and was it removed on time  (MONEY-C46)
- if something breaks or gets ransomed today, can we actually recover  (MONEY-C47)
- is our domain safe, and is someone impersonating us  (MONEY-C48)
- are we exposed on GDPR/CCPA or consent rules for where our customers are  (MONEY-C49)
- are we covering all four security pillars, and which PCI questionnaire actually applies to us  (MONEY-C50, MONEY-C74)
- can someone spoof our domain in an email right now  (MONEY-C72)
- which keys exist, who holds them, and which are overdue for rotation  (MONEY-C73)
- would our own staff catch a phishing attempt today  (MONEY-C75)
- did this vendor pass a risk check before it touched customer or payment data  (MONEY-C77)

### Metrics specified

- `open_findings_by_severity`: How many security issues are open right now, by how bad they are. count of findings with resolved_at empty, grouped by severity
- `finding_age_days`: How long an open finding has been sitting unresolved. today − opened_at, per open finding
- `bot_traffic_pct`: Share of site traffic that scores as automated. requests below the bot-score threshold ÷ total requests, by endpoint
- `card_testing_bursts`: Number of times card attempts spiked in a short window, a known fraud pattern. count of time windows where failed-auth attempts exceed the set per-minute threshold
- `chargeback_rate`: Share of orders disputed as chargebacks. chargebacks in period ÷ orders in period
- `dispute_rate`: Share of orders disputed on any channel, chargebacks plus PayPal/other processor disputes. (chargebacks + non-chargeback processor disputes) in period ÷ orders in period
- `return_to_sender_rate`: Share of shipped orders a carrier returned undelivered (refused, bad address, unclaimed), never reaching the customer. orders marked carrier return-to-sender in period ÷ orders shipped in period
- `rto_rate`: Share of COD orders that came back without the customer receiving them (India only; reads null for US brands). COD orders returned to origin in period ÷ COD orders dispatched in period
- `payment_method_mix`: Share of orders by payment method: card, Shop Pay, PayPal, Apple Pay, BNPL (Affirm, Klarna, Afterpay). orders by payment method in period ÷ total orders in period
- `cod_share`: Share of orders paid cash on delivery (India only; reads null for US brands). COD orders in period ÷ total orders in period
- `false_decline_rate`: Share of good orders wrongly blocked by fraud rules. declined orders later confirmed legitimate ÷ total declined orders
- `admin_2fa_coverage`: Share of admin accounts with 2FA or a passkey enabled. admin accounts with 2FA/passkey enabled ÷ total admin accounts
- `access_review_completeness`: Share of staff mapped to a least-privilege role with a recent review. staff with a role review in the last 90 days ÷ total staff with admin access
- `backup_restore_success`: Whether the last restore test actually worked, and when it ran. most recent backup_log row with restore_tested_at set, and its result
- `dns_dangling_records`: Number of DNS records pointing at something that no longer exists. count of dns_records with status = dangling
- `lookalike_domain_count`: Number of new domains that could be impersonating the brand. count of domain_watch rows registered in the period matching the brand's name pattern
- `email_auth_status`: Whether email from this domain can be spoofed. SPF present, DKIM present, DMARC policy (none/quarantine/reject), per sending domain
- `credential_rotation_overdue`: Number of API keys or tokens overdue for rotation. count of credential_inventory rows where today − last_rotated exceeds the set rotation schedule
- `pci_saq_status`: Which PCI self-assessment applies, and when it was last confirmed. current saq_type and days since confirmed_at, per payment flow
- `phishing_sim_click_rate`: Share of staff who clicked the last simulated phishing email. staff who clicked ÷ staff who received the simulation
- `vendor_risk_completion_rate`: Share of vendors with a completed risk check and signed data-processing agreement before data access. vendors with questionnaire complete and DPA signed before data_access_granted_at ÷ total vendors with data access

### Insights specified (rules in code)

- critical finding aging: a finding with severity critical has finding_age_days over 7 → "{finding} has been open {n} days past the 7-day fix window" (action MONEY-C44)
- checkout bot surge: bot_traffic_pct on a checkout-related endpoint rises more than the brand's own trailing baseline by 50% relative → "{pct}% of checkout traffic this week scored as bots, up from {baseline_pct}%" (action MONEY-C41)
- card testing detected: card_testing_bursts is above zero in the period → "{n} failed card attempts hit checkout in {window}, a card-testing pattern" (action MONEY-C42)
- chargeback rate rising toward flag: chargeback_rate is within 0.2 points of the processor's own flag threshold → "chargebacks are at {pct}, {gap} points under the processor's flag line" (action MONEY-C42)
- admin missing 2FA: admin_2fa_coverage is below 100% → "{n} admin accounts have no 2FA or passkey" (action MONEY-C43)
- backup restore untested: days since the last successful backup_restore_success exceeds 30 → "the last successful restore test was {n} days ago" (action MONEY-C47)
- dangling DNS record: dns_dangling_records is above zero → "{n} DNS records point at nothing and could be hijacked" (action MONEY-C48)
- lookalike domain registered: lookalike_domain_count is above zero in the period → "{n} new lookalike domains were registered this month" (action MONEY-C48)
- DMARC not enforcing: email_auth_status shows dmarc policy as none or quarantine on a sending domain → "DMARC on {domain} is not set to reject, so spoofed mail is not blocked" (action MONEY-C72)
- credential overdue: credential_rotation_overdue is above zero → "{n} API keys have not been rotated in over {days} days" (action MONEY-C73)
- return abuse pattern: a customer's return_count_90d exceeds the brand's own set threshold for orders in the same window → "{customer} has returned {n} of their last {m} orders" (action MONEY-C76)
- vendor risk gap: a vendor's data_access_granted_at is set but questionnaire_status is not complete or dpa_signed is false → "{vendor} got data access before its risk questionnaire was finished" (action MONEY-C77)

### Visuals specified

- finding severity funnel (stacked bar with age overlay): open findings by severity and how long each has been open
- bot traffic trend (line chart, checkout vs site-wide): bot traffic share over time, checkout endpoints separated from the rest of the site
- admin access matrix (heatmap, staff by admin area): who has access to what, and whether 2FA is on
- backup and restore calendar (calendar strip): every backup run and the last successful restore test date
- credential rotation age table (table, heat-colored by age): every API key or token and days since last rotation
- domain and DNS risk list (list with severity tags): dangling DNS records and new lookalike domains found this period

### Not in the usual tools

- open findings from the weekly scan tracked with age against a fix window and a named owner, in the same room as everything else
- bot traffic separated for checkout endpoints and tied to fraud and order-count anomalies
- backup health shown as a tested restore date, not just a backup existing
- domain, DNS and lookalike-domain risk watched together with the brand's own registrar lock state
- credential rotation tracked with an overdue flag against a set schedule
- account-takeover signals correlated across Shopify admin, ad accounts, the ESP and the payment processor in one place

### Data this screen needs

- `security_scan_findings`: finding_id, severity, area, opened_at, resolved_at, owner (weekly automated scanner)
- `bot_traffic`: date, endpoint, bot_score_bucket, request_count (Cloudflare bot analytics)
- `fraud_signals`: date, event_type, count, amount (payment gateway/processor logs)
- `admin_access`: user, role, area, twofa_enabled, last_login, location, device (platform admin logs (Shopify, Meta, ESP))
- `backup_log`: backup_id, location, taken_at, restore_tested_at, result (backup provider export)
- `dns_records`: domain, record_type, target, status, checked_at (DNS audit script)
- `domain_watch`: lookalike_domain, registered_at, risk_score (brand monitoring script)
- `email_auth`: domain, spf, dkim, dmarc_policy, checked_at (DNS lookup script)
- `credential_inventory`: key_name, service, holder, last_rotated, rotation_due (manual or secrets vault export)
- `pci_scope`: payment_flow, saq_type, confirmed_at (manual assessment)
- `phishing_sim`: staff_id, sent_at, clicked, reported (training platform export)
- `return_abuse`: customer_id, order_id, return_reason, return_count_90d, flagged (Shopify returns + CS data)
- `vendor_risk`: vendor, questionnaire_status, dpa_signed, data_access_granted_at (manual vendor register)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
| 0 | 0.1 to 0.4 | 2026-09-28 | shell, api, 3 tiles, 2 insight rules, 1 chart, audit |

## Round 0 status

1. Built: index.html, screen.js, api.py (overview, findings), audit.py (22 rules, RULES list), tests/test_screen_security.py (13 tests pass).
2. Tiles: chargeback rate 0.08 percent (lines 0.15, 0.65, 0.9), dispute win rate 60.6 percent (20 of 33), 7 vendor scripts (line 5).
3. Insights as rules: chargeback lines with win rate and scaled payout dispute moves; storefront surface (scripts, tag manager, consent, captcha, agent endpoint).
4. Chart: chargebacks and inquiries per 1,000 paid orders, 12 months, against the 1.5 per 1,000 alert line.
5. Findings on Bombas: SEC-R08 and SEC-R11 open (medium); 15 unavailable with the connector named; money computed in code for R01 and R02 when they fire.
6. Gaps: bot, card testing, promo abuse, account takeover, scans, DNS, email auth and payout holds read unavailable; all data simulated, labelled on the page.
