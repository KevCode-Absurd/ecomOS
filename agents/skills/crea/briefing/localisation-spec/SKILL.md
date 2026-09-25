---
name: briefing/localisation-spec
owner: crea-paid-creative-copy
version: 1
invoke_when: creative or copy needs specifying for a target market and
  device with its own payment, delivery and language norms
inputs: brand brain market policies, device target
outputs: target spec sheet: device, trust facts, language notes, market tag
---
Purpose: fix the real, checkable local facts a creative or copy set must use,
so a market-specific ad never carries the wrong market's assumption by
accident.

Steps
1. Confirm the device target: the US default is standard feed and story
   formats; a market whose traffic skews mobile-first (for example an
   India-facing brief) defaults to vertical-only formats instead.
2. Pull the market's real trust facts from the brand brain: the payment
   method mix (card, Shop Pay, PayPal, Apple Pay, BNPL such as Affirm,
   Klarna or Afterpay for a US brand; COD availability and EMI where the
   target market runs them, markets: IN), the actual delivery window, and
   which local payment logos are true to show.
3. Note the language pair and whether the persona's real speech pattern
   calls for a dual-language, code-switched hook (for example a natural
   Hindi-English mix for an India-market brief) rather than a straight
   translation.
4. Flag any trust line inherited from a source market that does not hold
   here: a foreign-currency guarantee, a shipping time that does not apply,
   a payment method not actually offered.
5. Set the market tag that every downstream asset in this run must carry, so
   it can never be accidentally served to the wrong market.

Checks: every fact traces to current policy, not assumption; device target
stated.

Output: the target spec sheet, feeding the localisation workflow's copy and
resize steps.

Example, US brand: spec confirms the payment mix is card, Shop Pay and
Klarna, delivery is 3 to 5 business days, and any inherited COD or EMI line
is dropped since it does not apply. Example, India-market brief (markets:
IN): spec confirms COD is offered, EMI starts at a stated amount, and the
US "free returns within 30 days" line is replaced with the real local
return window.
