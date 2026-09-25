---
name: git-ci-pipeline
owner: site-specialist
version: 1
invoke_when: setting up or maintaining git-based theme version control, CI linting, or a staging mirror of production
inputs: current theme files, GitHub repo access, Shopify CLI
outputs: git repo with commit history, CI config, staging theme URL, rollback runbook
---
# Git-based theme version control and CI

## Purpose
Replace duplicate-theme-in-admin editing with a real engineering workflow, so every change is reviewable by commit and reversible by command, not by remembering which duplicate is which.

## Steps
1. Connect the theme repo to GitHub and configure Shopify CLI for local development.
2. Add theme-check linting to run on every commit and block a merge on a hard error.
3. Stand up a staging theme URL that auto-deploys from a branch, mirroring production.
4. Require a second reviewer or the founder gate before any merge to the live theme.
5. Keep one tested command to redeploy the previous commit's theme package.
6. Tag each deploy with the change brief it shipped so the registry can trace it to an approved idea.
7. Refresh the staging store's product/price/inventory snapshot from production on a schedule, never the reverse.

## Checks
- Rollback has actually been exercised once, not just written down.
- Staging always mirrors current production data before a risky test.

## Output
A git repo with real commit history, working CI config, a live staging theme URL, and a rollback runbook.

## Example
"Deploy tagged to brief DEV-2026-091. Rollback tested: `shopify theme push --release=prev` restored the prior theme in 40 seconds."
