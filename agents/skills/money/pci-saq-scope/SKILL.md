---
name: money/pci-saq-scope
owner: MONEY
version: 1
invoke_when: checkout payment flow changes or the annual PCI self-assessment is due
inputs: checkout payment flow diagram, gateway integration method, prior SAQ
outputs: payment flow map, applicable SAQ type, scope confirmation, completed SAQ draft
---
# Confirm PCI DSS scope and complete the SAQ

## Purpose
Keep raw card data out of the brand's own systems and complete the right self-assessment questionnaire for the flow that actually exists.

## Steps
1. Map exactly how checkout takes payment: a gateway-hosted field, a redirect, or a direct API integration.
2. Determine which SAQ type applies to that exact flow, not the type the gateway's marketing suggests.
3. Confirm with a live checkout trace that raw card data never touches the brand's own servers outside the confirmed scope.
4. Complete the SAQ's factual items from the confirmed scope and flow.
5. Flag any item needing a signature or a third-party attestation for a person to complete.

## Checks
- Scope is confirmed by tracing a live checkout, not by reading settings alone.
- No signature or attestation is provided by this skill; submission stays with a person.

## Output
The payment flow map, the applicable SAQ type, the scope confirmation, and the completed SAQ draft.

## Example
A checkout believed to be fully hosted by the gateway is found, on a live trace, to pass a card's last 4 digits through the brand's own order confirmation email template; the scope confirmation flags this before the SAQ is finalized.
