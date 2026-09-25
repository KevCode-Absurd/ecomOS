---
name: whatsapp-buy-flow
owner: site-specialist
version: 1
markets: IN, EU, LATAM (reads null, does not run for a US-default brand)
invoke_when: COD or trust-driven checkout hesitation is diagnosed as a bottleneck in a WhatsApp-commerce market (India, EU, LATAM)
inputs: WhatsApp Business catalog access, PDP template
outputs: click-to-WhatsApp button, synced catalog, click-to-order attribution
---
# Click-to-WhatsApp catalog and buy flow (India, EU, LATAM market option)

## Purpose
Give a trust-hesitant shopper in a WhatsApp-commerce market a pre-purchase chat channel on the exact SKU they're viewing, without taking over the conversation itself, which belongs to Lifecycle. This option reads null and does not run for a US-default brand.

## Steps
1. Sync the live product catalogue (price, stock, variant) to the brand's WhatsApp Business catalog on a schedule.
2. Add a click-to-WhatsApp button on the PDP that pre-fills the exact SKU, variant and a template question.
3. Confirm the button appears only in markets where WhatsApp commerce is legal and commonly used (India, EU, LATAM), never for a US-default brand.
4. Measure how many PDP-to-WhatsApp clicks convert to an order, tracked separately from normal add-to-cart.
5. Hand the WhatsApp conversation flow itself, cart recovery and support scripting to the Lifecycle specialist.

## Checks
- WhatsApp-originated orders never double-count against add-to-cart in reporting.
- The button never appears in a market where it hasn't been confirmed appropriate.

## Output
A working click-to-WhatsApp button, a synced catalog, and click-to-order attribution data.

## Example
"Click-to-WhatsApp button added to the top 20 SKUs by COD share in the brand's India market; 340 clicks in month one, 41 converted to an order via the WhatsApp flow Lifecycle built, tracked as its own attribution source."
