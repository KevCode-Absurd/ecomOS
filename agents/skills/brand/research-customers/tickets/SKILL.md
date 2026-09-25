---
name: research-customers/tickets
owner: BRAND
version: 1
invoke_when: the source is support tickets, returns or call transcripts
inputs: support desk export, returns log
outputs: struggle theme list, draft macro updates, quote set with consent flag
---
# Mine support tickets

## Purpose
Support tickets are passive evidence of the customer's real struggle, separate from anything they said to make a sale. This skill turns that raw text into themes and support-macro material without exposing private customer data downstream.

## Steps
1. Export tickets, return reasons and call transcripts for the period from the support desk connector.
2. Tag each item by the underlying job or failure (a size mismatch, a delivery delay past the pincode's normal window, a fabric-care confusion), never by the customer's exact wording alone.
3. Cluster repeated patterns; a single ticket is an anecdote, three or more with the same root cause is a pattern.
4. For each named, repeated objection, draft an update to the standing support macro that answers it.
5. Flag sizing, fit or fulfilment anxieties specifically, since these often feed a dedicated confidence angle in copy.
6. Log the consent status of every ticket before any quote leaves the ticket system; a ticket with no consent basis is summarized, never quoted verbatim.

## Checks
- Every quote used downstream carries a consent flag.
- Themes are tagged by underlying cause, not by the customer's literal words alone.
- COD refusal or regional delivery-delay patterns are kept separate from product-quality patterns; conflating them misleads the avatar record.

## Output
`{struggle_theme_list: [...], draft_macro_updates: [...], quote_set_with_consent_flag: [...]}`

## Example
Theme: "sizing confusion, cross-body strap length" (9 tickets in 30 days) -> macro draft added: a strap-length chart link in the auto-reply for that product tag.
