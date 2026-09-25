---
name: make-content/pinterest-pin
owner: ORG
version: 1
invoke_when: a task needs a single pin drafted, or the monthly board and trend review is due
inputs: approved image/video, keyword and question map, current board architecture, brand voice file
outputs: pin title/description/board/destination, or a board review with retire/add list
---
# Pinterest pin and board strategy

## Purpose
Pinterest is a visual search engine, not a feed; this skill writes for the search box first, and separately keeps the board architecture matched to how buyers actually search, reviewed monthly.

## Steps
1. Identify the exact phrase a buyer would type into Pinterest search for this image or topic.
2. Write the pin title (under 100 characters, keyword first) and a natural-sentence, keyword-rich description, never a keyword stack.
3. Pick or create the matching board; board titles use buyer search terms, not internal category names.
4. Set the destination link to a live page that matches the pin's promise; never the homepage.
5. Monthly (scope: board): pull board-level impressions, retire or merge boards with none, and add one board for a rising search term found in the keyword map.

## Checks
- Title and description both carry the target search phrase.
- Destination link is live and on-topic.
- No board created without a supporting search-volume signal.

## Output
{scope, pin{}, board_review{}}

## Example
Pin title: "Foldable baby stroller for small US apartments" -> board "Small-space baby gear ideas", linking to the collection page, not the homepage.
