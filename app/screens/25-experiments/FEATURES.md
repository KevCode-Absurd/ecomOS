# Experiments and memory: features

Status: todo | doing | done | parked. One feature per commit. The first round is the skeleton; after that, features come in rounds of 10, stack-ranked by revenue impact, usefulness and how easy they are to build on dummy data.

## Round 0: skeleton

| # | Feature | Status |
|---|---|---|
| 0.1 | Page shell in the shared UI kit: header, empty-state tiles, insight list, action buttons | todo |
| 0.2 | `api.py` serving this screen's metrics from `app/data/` with unavailable states | todo |
| 0.3 | 3 metric tiles, 2 insights, 1 chart from the sample brand | todo |

## Candidates from the room spec (pick 10 per round)

### Questions this screen should answer

- what are we actually testing right now  (REG-C03)
- what result am I waiting on, and is anything late  (REG-C08, REG-C02)
- did it work, in numbers I can read in one line  (REG-C03)
- does this idea actually work for this brand, based on our own history  (REG-C04)
- what did we put off, and is it time to look again  (REG-C05)
- are two experiments about to step on each other  (LOOP-C35)
- did we actually agree what winning and losing look like before we started  (LOOP-C08)
- why is a web idea beating a bank idea, or vice versa  (LOOP-C09)
- why does the system already know I don't like ideas like this  (LOOP-C10)
- would the top pick actually be my pick  (LOOP-C36)
- what did we learn, and would we do it again  (LOOP-C25)
- why did we do it this way, for someone new joining  (LOOP-C10)

### Metrics specified

- `running_count`: How many ideas are currently running for this brand. count of registry entries with status = running
- `reads_due_this_week`: How many running entries hit their read point this week. count where read_point falls within the current week
- `stale_entries_count`: Entries past their read point with no result recorded yet. count where today > read_point and result is null
- `parked_count`: How many ideas are parked, and how many have an expiring reason. count of status = parked; subset where expiry date <= today
- `result_distribution`: Share of read results that were up, down, flat or unreadable. count by result value / total results in window
- `brand_prior_effect`: This brand's own updated effect size for an idea, after being tried here. weighted average of this brand's own recorded results for the idea, most recent weighted higher
- `founder_weight_table`: The standing weights the ranker applies, built from repeated founder reasons. reason-to-weight mapping, fixed table, updated when a reason repeats
- `overlap_count`: Pairs of running entries sharing an audience or metric window. pairwise overlap check across running entries
- `prediction_accuracy_pct`: How often the predicted founder decision matched the actual one. matches / total predictions made
- `retro_completion_rate`: Share of closed initiatives that got a retro. initiatives with a retro note / initiatives closed
- `read_point_sizing`: Whether each running entry's read point is sized to the metric's own noise, not a fixed day count. flag where read_point duration falls below the minimum days needed for that metric type per LOOP-C08
- `handoff_ready_count`: How many areas have an exportable, plain-language decision history ready for a new person. count of areas with a generated handoff export in the last 90 days

### Insights specified (rules in code)

- read point reached: today equals or passes an entry's read_point → "{idea} on {brand} hit its read point; result is {up_down_flat_unreadable}: {number}" (action REG-C03)
- stale unread entry: today exceeds read_point by more than a few days with no result recorded → "{idea} passed its read point {n} days ago with no result recorded yet" (action REG-C02)
- parked reason expired: a parked entry's stored expiry date has passed → "{idea} was parked because '{reason}'; that reason has now expired" (action REG-C05)
- unreadable result: a read point landed but required data is missing → "{idea}'s read is unreadable: {field} is missing, not zero" (action REG-C03)
- overlap collision: two running entries share an audience or metric window → "{idea_a} and {idea_b} collide on {dimension}; stagger one" (action LOOP-C35)
- repeated reject reason becomes weight: the same founder reason appears 3 or more times against similar idea attributes → "'{reason}' has come up {n} times; ideas like this now rank lower automatically" (action LOOP-C10)
- ranked pick versus prediction mismatch: the code ranker's top card and the predicted founder decision disagree → "The top-ranked card is a likely {predicted_decision} based on your past reasons; it is shown anyway" (action LOOP-C36)
- read point too small: an entry's read point duration is below the minimum for its metric type → "{idea}'s read point is sized too short to reach a real signal for {metric}" (action LOOP-C08)
- retro missing: an initiative closed with no retro note filed → "{initiative} closed {n} days ago with no retro filed yet" (action LOOP-C25)
- brand prior updated: a new result changes the brand's own weighted effect estimate for an idea → "{idea} now shows a {new_estimate} effect on this brand, based on {n} attempts" (action REG-C04)
- would-we-again check: a retro's stored answer to 'would we do this again' is no → "The retro for {initiative} says we would not do it the same way again: {reason}" (action LOOP-C25)

### Visuals specified

- registry kanban (kanban-style board): entries grouped by status: running, waiting, parked, done, with brand tags for an agency view
- read point timeline (horizontal timeline): upcoming and overdue read points across all running entries
- brand prior sparkline (small multiples of sparklines per idea): how the brand's own effect estimate for an idea has moved across repeated attempts
- overlap matrix (matrix / network diagram): which running entries share an audience or window with which others
- founder reason weight chart (horizontal bar chart): the most common founder reasons and the ranking weight each has earned
- retro scorecard (checklist-style card): what worked, what did not, and the would-we-again answer for each closed initiative

### Not in the usual tools

- a per-brand prior effect size for a marketing idea, built only from what happened when this brand tried it, separate from the bank's brand-agnostic basis
- a founder's repeated approve, reject or park reason turned automatically into a ranking weight, without being asked to restate it
- an overlap check across marketing ideas from a bank, an audit and the web, not just inside one engineering team's own test list
- the same retro shape (what worked, what did not, would we do it again) applied automatically to any closed initiative type: launch, crisis, onboarding, replatform

### Data this screen needs

- `registry_entries`: id, brand, idea_id, source, status, owner, artefact_link, metric, read_point, audience (registrar)
- `brand_priors`: brand, idea_id, attempts, weighted_effect, last_updated (REG-C04)
- `reasons_table`: reason_text, attribute_tags, weight (fixed code table)
- `agency_overlay`: idea_id, store_tags, direction, opt_out_flag (REG-C06)
- `overlap_flags`: brand, entry_a, entry_b, dimension, detected_date, resolved (LOOP-C35)
- `prediction_log`: brand, card_id, predicted_decision, reason_pattern, actual_decision (LOOP-C36)
- `initiative_retros`: brand, initiative_id, type, what_worked, what_didnt, would_again, checklist_version (LOOP-C25)
- `handoff_exports`: brand, area, generated_date, content_ref (LOOP-C10 extension)

## Rounds

| Round | Features picked | Date | Notes |
|---|---|---|---|
