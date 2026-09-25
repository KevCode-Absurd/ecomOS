---
name: speed-audit
owner: site-specialist
version: 1
invoke_when: capturing a speed baseline, writing the resulting brief, running monthly regression monitoring, or prepping for a sale's peak load
inputs: brand brain top landing/PDP URLs, connector: pagespeed insights api, results/*.json history
outputs: baseline measurement, root-cause diagnosis, developer brief, founder decision page, monthly trend report, peak readiness report
---
# Speed measurement, baseline and monitoring

## Purpose
Measure real page speed honestly, fix the page paid traffic actually lands on first, and keep a running budget so nothing regresses silently.

## Steps
1. Record every response of the real page with speed_lab.record before changing anything.
2. Measure 3 runs on a throttled mobile profile (Pixel 5, slow 4G, 4x CPU) and take the median.
3. Cross-check a suspicious lab result against PageSpeed Insights field data.
4. Fix the page paid ads land on before any other template.
5. Turn every diagnosed fix into a brief: what, needs, tradeoff, who, a numeric pass threshold, and a one-step rollback.
6. Re-audit monthly holding a page-weight and script-count budget, flagging the moment a budget is crossed.
7. Wait about 28 days of field data before calling a fix a win.
8. Before a known sale, list at-risk dynamic steps, load-test them, and freeze risky changes during the window.

## Checks
- Every measurement is 3 runs averaged, never 1.
- Field and lab data are read as separate things, never conflated.
- Every brief's threshold is a number, never a feeling.

## Output
A baseline measurement file, a diagnosis, a developer brief per fix, a monthly trend report, and (seasonally) a peak-readiness report.

## Example
"PDP LCP: 4.1s baseline (median of 3 runs). Fix: preload hero image, cut a blocking script. Threshold: LCP under 2.5s. Rollback: remove the preload tag, one line."
