---
name: money/security-audit-quarterly
owner: MONEY
version: 1
invoke_when: the quarterly four-pillar security audit needs running
inputs: staff roster, admin role map, privacy policy, sending domains, API key inventory, admin-access list
outputs: access audit, privacy compliance check, email-auth status, credential rotation log, training result, by pillar
---
# Run the quarterly four-pillar security audit

## Purpose
Run the recurring program with a named owner per pillar, so nothing waits for an incident to get checked.

## Steps
1. Map every staff role to only the admin areas it needs, run the full access audit, and confirm same-day offboarding for any recent exits.
2. Confirm GDPR/CCPA exposure by customer location and publish a privacy policy and consent banner covering AI-agent interactions.
3. Check SPF, DKIM, DMARC and BIMI on every sending domain and move DMARC from monitor-only toward enforced where safe.
4. Rotate API keys, tokens and service credentials on schedule and immediately on any staff exit.
5. Run a phishing simulation and short security training for every staff member with admin access, tracking who clicks, who reports, and who needs a repeat.
6. Confirm any platform SOC or PCI claim before it is repeated, and maintain the hosted-versus-self-hosted responsibility map.

## Checks
- Offboarding is confirmed, never assumed complete.
- DMARC's exact policy state (none, quarantine, reject) is stated, not summarized as 'set up'.
- Every admin-access staff member has a tracked training result.

## Output
The requested pillar's result, rolled into the quarterly security scorecard with a named owner per pillar.

## Example
A staff member who left 2 months ago still has an active API key; the credential rotation check catches it and the fix list names the exact key to revoke today, not at the next scheduled rotation.
