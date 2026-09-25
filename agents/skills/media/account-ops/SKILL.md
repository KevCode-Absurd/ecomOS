---
    name: account-ops
    owner: media-buyer
    version: 1
    invoke_when: the job is about account health, not building a campaign
    inputs: brand brain account inventory, sale calendar, markets served
    outputs: routes to the correct operations sub-skill
    ---
    Purpose: hold the audits, access, calendar and QA jobs that keep the whole
    account trustworthy, apart from the campaign-building tree, so they are not
    confused with a build task.

    Steps
    1. Read the operational job named: audit, access, cross-border setup, sale ramp,
       incrementality test, suggestion filter, or pre-launch QA.
    2. Route to the matching sub-skill.
    3. Every sub-skill here reports findings ranked by money at stake, with a
       source, not a list of equal-weight observations.

    Checks
    - Every finding traces to a number and a source (brand record, platform read,
      or a dated public URL).
    - No sub-skill here proposes a live write; each hands back a report, a change
      list, or (for a founder_gate job) a decision brief.

    Output: a routing decision to one operations sub-skill.

    Example: task says "it's the first week of October, Diwali sale is in 3 weeks."
    -> routes to `media/account-ops/peak-sale-ramp`.
