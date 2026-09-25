---
name: core-web-vitals-fix
owner: site-specialist
version: 1
invoke_when: a page's CLS, LCP or INP score needs a named root cause and a fix, not a general speed pass
inputs: baseline measurement, recorded page or filmstrip, the metric in question
outputs: per-template diagnosis and fix sequence for the named metric
---
# Diagnose and fix CLS, LCP and INP

## Purpose
Turn a Core Web Vital score into a named element and a fix, since a score alone tells nobody what to change.

## Steps
1. For layout shift (CLS): name the exact element causing the shift, reserve space for anything arriving after first paint, fix contradicting CSS, and remove fade-in effects.
2. For largest contentful paint (LCP): name the LCP element per template, check time-to-first-byte before blaming the image, then run the fix order in sequence: un-lazy, de-animate, compress, preload, cut the blocking script hiding it.
3. For interactivity (INP): cut main-thread JavaScript blocking add-to-cart, variant pickers, filters and search autocomplete; treat autocomplete lag as a real issue, not a shrug.
4. Confirm every fix on a real device: a filmstrip re-run for CLS, a preload/priority check for LCP, a real tap test for INP.
5. Run check_fidelity so the fast variant is still the same page as the baseline.

## Checks
- The shifting element, LCP element, or blocking script is named specifically.
- INP fix confirmed by a real tap test, not the lab score alone.
- Fidelity check passed before any number is trusted.

## Output
A per-template diagnosis naming the exact cause, and the fix sequence that was run, with before/after numbers.

## Example
"LCP element: hero image, hidden by a 400ms fade-in script. Fix order: removed fade-in, preloaded image with fetchpriority=high. LCP 3.8s to 1.9s, median of 3 runs, fidelity confirmed."
