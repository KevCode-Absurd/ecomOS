---
name: production-planning
owner: ORG
version: 1
invoke_when: the monthly calendar needs a real shoot schedule, or founder camera capacity is unconfirmed
inputs: draft calendar, founder's stated available days, current lighting/location setup
outputs: shoot schedule mapped to calendar slots, fast-turnaround formats for founder-only days
---
# Production planning: founder camera time and batching

## Purpose
Combine two practical constraints into one plan: how much the founder can be on camera this month, and fixed batching days the team can hold without chasing a free hour, so the calendar does not stall on logistics.

## Steps
1. Split calendar slots into founder-dependent and team-filmable.
2. Confirm the founder's available days for the month; a founder-dependent slot with no confirmed date is flagged, not scheduled.
3. Set fixed batching days on a repeating cadence.
4. Set the default lighting/backdrop for routine posts; flag any slot where raising production stakes (a real location) is justified by past performance of that format.
5. Build a fast-turnaround format (single phone, one location, under 20 minutes) for days only the founder can film.
6. Map each slot to a date, location and lighting note.

## Checks
- Every founder-dependent slot has a confirmed date or is flagged, not silently scheduled.
- Batching days repeat on a fixed pattern.
- Every shoot day has a lighting/location note.

## Output
{shoot_schedule[], fast_turnaround_formats[]}

## Example
Batching day: first Tuesday of the month, 4 slots, standard kitchen-counter lighting; founder-only slot on the 14th uses the fast-turnaround format because no team member is free that day.
