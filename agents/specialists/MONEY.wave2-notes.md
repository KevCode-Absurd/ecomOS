# MONEY wave 2 notes

## Wave 5 update (US-first)
This file is the original wave-2 research log and is left as a historical
record of what was actually searched and cited at the time, including the
India-specific sources below. The capability, workflow and skill records
themselves have since been rewritten wave-5 to make a US brand the default
(nexus-by-state sales tax through Avalara/TaxJar, Gusto/ADP payroll,
Shopify Payments/Stripe/PayPal/Amazon payout reconciliation, chargeback
representment as its own capability), with the India-specific mechanics
below (GST/HSN/e-invoice/GSTR, COD/RTO courier remittance, PF/ESI/TDS
payroll) kept as a market option that reads null for a US-only brand. Read
this file as "what wave 2 found," not as the current spec.

## Method
20 web searches, 1 page fetch (ecombalance.com's 17 bookkeeping duties list). Slightly over the 10-14 search guide because the domain spans four sub-areas (finance, analytics, ops, security) and each needed at least 2 searches to cover job descriptions, tools and India specifics without guessing.

## Sources by type
- Job descriptions / day-in-the-life: bookkeeper (Indeed, ecombalance), fractional CFO (Eightx, Finaloop), marketing ops manager (ShipBob, Zippia), chief of staff (Voltage Control, Hirechore).
- Agency and service-menu pages: fractional CFO retainers (Eightx), insurance brokers (Vouch, Mercury), contract management (Ironclad).
- SaaS/tool feature lists: A2X, Link My Books, Webgility, Synder (marketplace settlement), Ramp, Bill.com, Ottimate (AP), Zeni, Digits, Puzzle, Docyt (AI bookkeeping), Signifyd, Riskified, Forter, Sift (fraud), Daasity, Triple Whale, Polar Analytics (ecommerce analytics/warehouse), Doppler, 1Password (secrets), Vendr, Ironclad (SaaS/contract management), ClickPost, Shipway (India logistics/COD).
- Freelance marketplace gigs: Fiverr accounting-services category (ecommerce bookkeeping, payroll, GST-adjacent work).
- AI agent products: Zeni/Digits/Puzzle AI categorization agents, Triple Whale Moby and ThoughtSpot Spotter as ask-the-data analysts, Ramp's AP Agent.
- India-specific: GST e-invoicing/e-way bill/GSTR software (GSTZen, GSTHero), PF/ESI/TDS payroll compliance (RazorpayX, Keka), Flipkart/Myntra settlement mechanics (commission, Section 52 TCS, T+5/T+7 payout), COD/RTO remittance via courier aggregators.

## What wave 1 missed most
Wave 1 is strong on the *judgment* layer (margin models, forecasts, audits, frameworks) but thin on the *mechanical* layer underneath it: nobody in wave 1 does the actual bookkeeping transaction posting, AP/AR processing, payroll statutory filing, fixed-asset tracking, or the GST filing mechanics (e-invoice, e-way bill, GSTR-1/3B, ITC reconciliation) as opposed to tracking where liability exists. The India settlement layer (marketplace fee unbundling, COD remittance aging) was also absent. On the ops side, wave 1 covers hiring *frameworks* and vendor *selection* but not the follow-through: sourcing/screening, onboarding provisioning, contractor lifecycle, contract redlining, offboarding, and 3PL day-to-day SLA monitoring. On security, wave 1 covers site-facing controls (checkout fraud, admin access, web app defects) but missed email authentication (SPF/DKIM/DMARC), secrets/API-key rotation, PCI SAQ scope, security awareness training, return-fraud detection, and vendor data-processing risk. On analytics, wave 1 covers tracking audits and reconciliation but not building the warehouse/ETL itself, an ask-the-data analyst, marketing mix modeling, or RFM segmentation.

## What is possible but not sold yet
Four records (found_in: possible): auto-drafting SaaS renewal renegotiation emails from real usage data before the notice window closes, rather than a static audit; auto-escalating an aged payout remittance (gateway, marketplace, or a courier for India COD) to its ops contact with the specific order IDs and SLA clause cited, rather than a dashboard someone has to act on (this was originally scoped narrowly to India COD remittance and is now generalized in MONEY-C79, with COD kept as the India option); running a live cash-forecast simulation against a proposed financing structure in the same session a founder asks about it, instead of a one-time comparison memo; and correlating account-takeover signals across every admin-level system at once (Shopify, ad accounts, ESP, payment processor), which no single point tool sees today because each only watches its own logins.
