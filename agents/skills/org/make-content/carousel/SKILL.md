---
name: make-content/carousel
owner: ORG
version: 1
invoke_when: the task's format is a multi-slide carousel (Instagram or LinkedIn)
inputs: brand voice file, claims tiers, one named SKU or topic, one named buyer
outputs: hook slide, body slides, closing slide, caption, CTA, claims list, a design-ready slide list
---
# Carousel script and slide list

## Purpose
Give design a slide-by-slide brief for one argument (a comparison, a myth-bust, a how-to), sized to finish in 5-9 slides so swipe-through does not drop off.

## Steps
1. Pick the single argument the carousel makes. One carousel, one point.
2. Write slide 1: the hook, readable in under 2 seconds, stating the stakes.
3. Write slides 2 through 7-9: one idea per slide, short lines, one heading plus one supporting line each.
4. Write the closing slide: a one-line recap and one CTA.
5. Write the caption for readers who read captions before swiping; apply the same claims tiers.
6. List every slide's heading, supporting text and image direction for the designer.

## Checks
- One idea per slide, no slide carrying two arguments.
- Every factual line is claims-tier checked.
- Total slides between 5 and 9.

## Output
{hook_slide, slides[], closing_slide, caption, cta, claims_used[]}

## Example
Argument: "Why our hinge outlasts the $40 stroller." Slide 3 heading: "200,000 fold cycles tested", supporting: "our lab number, dated March 2026".
