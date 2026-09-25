---
name: money/security-audit-monthly
owner: MONEY
version: 1
invoke_when: the monthly authentication, web-app and backup audit needs running
inputs: admin login config, checkout code access, backup schedule, incident runbook
outputs: auth audit, web-app defect and fix list, backup and restore test result, updated runbook
---
# Run the monthly auth, web-app and backup audit

## Purpose
Confirm the controls that stop an account takeover or a site defect from becoming a real incident, and prove a backup actually restores.

## Steps
1. Audit login, session and MFA design: 2FA or passkeys for every admin, session-cookie attributes, password hashing and rate limiting, and enumeration prevention on login and reset flows.
2. Audit storefront and checkout code for XSS, injection, CSRF, clickjacking, CORS and postMessage defects.
3. Confirm daily versioned backups exist in 3 separated locations with a ransomware-safe, offline copy.
4. Test a restore end to end this month, not just confirm the backup exists.
5. Update the unified incident runbook covering breach, skimmer and ransomware scenarios.

## Checks
- 2FA is confirmed by a live check, not assumed from a settings screenshot.
- A restore test actually opens a restored file; it is not just a scheduled job that ran.

## Output
The auth audit, the web-app defect list with a developer fix list, the backup and restore test result, and the updated runbook.

## Example
A scheduled backup has run every night for 6 months but the restore test this month fails silently on a corrupted archive; the audit catches it before an actual incident would have.
