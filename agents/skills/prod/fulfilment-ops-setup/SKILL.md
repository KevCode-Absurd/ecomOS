---
name: prod/fulfilment-ops-setup
owner: PROD
version: 1
invoke_when: a domestic fulfilment 3PL/WMS needs selecting, or warehouse and returns operating rules need setting
inputs: order volume and SKU count, SLA requirements, the candidate 3PL list, return/RTO volume and reasons
outputs: a negotiated SLA and tested WMS integration, slotting and staffing rules, and a fixed returns-grading rule
---
# Select 3PL/WMS and build warehouse and returns operations

## Purpose
Three related decisions belong to one fulfilment manager: which 3PL and WMS to run on, how the warehouse actually
operates day to day, and what happens to every unit that comes back. Keeping them together avoids a WMS chosen
without the warehouse rules it needs to support, or a returns rule invented case by case after go-live.

## Steps
1. Run the RFP and SLA negotiation for a domestic fulfilment 3PL: separate from any import-side freight or factory
   3PL, since the requirements differ (last-mile speed and accuracy versus long-haul cost).
2. Test the 3PL's WMS integration before go-live: order sync, stock sync, and returns feed, all tested end to end.
3. Set slotting rules by SKU velocity (fast movers closest to pack stations) and the pick-pack-QC method and
   staffing level against real, not projected, order volume.
4. Design a fixed rule for what happens to every returned unit: RTO or customer return: restock, refurbish, or
   write off, decided in advance rather than case by case, and apply it on a set schedule.
5. Review staffing levels and grading outcomes weekly against the plan.

## Checks
- The 3PL is chosen on SLA terms and service history, not the lowest quote alone.
- Go-live never happens before the WMS integration test passes.
- The grading rule is fixed and decided in advance, never improvised per return.

## Output
{sla, integration_test_result, slotting_rules, staffing_plan, grading_ruleset}

## Example
3PL selected on a 96% on-time SLA history despite a 5% higher quote. Integration test passed on stock sync;
returns feed needed a fix before go-live. Grading rule: RTO with unopened seal restocks automatically; opened
seal goes to refurbish queue; anything past 60 days is written off.
