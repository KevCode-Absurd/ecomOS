---
    name: meta-structure
    owner: media-buyer
    version: 1
    invoke_when: spend tier changed, an audit flagged structure, or naming is asked for
    inputs: trailing 30-day spend, catalogue, personas, audit output
    outputs: structure diagram, naming convention, change list
    ---
    Purpose: pick the Meta account shape that matches current spend and make every
    campaign and ad set readable by its name alone, so a reporting problem gets
    fixed with a rename, not a new campaign.

    Steps
    1. Place the account in its spend tier from trailing 30-day spend.
    2. Apply that tier's template: small gets one testing campaign; mid gets 2-3
       cold campaigns each with a written reason; large gets a page strategy and
       bidding diversity across campaigns.
    3. Merge campaigns too thin on conversions to optimise; fully consolidate a
       single-product, single-persona, small-spend store to one campaign.
    4. Write one defendable purpose line per campaign.
    5. Set the ad set naming pattern (persona, angle, offer, content type, launch
       date) and apply it to every existing and new ad set, including forks.

    Checks
    - Every campaign has a purpose line and every ad set follows the naming pattern.
    - No campaign exists only because of a launch date, not a business reason.

    Output: structure diagram + naming convention doc + change list for a human to
    apply in Ads Manager.

    Example: a brand crosses from $8k to $14k/month spend -> moves from the small
    template (one testing campaign) to the mid template (2 cold campaigns, one for
    bestsellers and one for a new SKU, each with a written reason).
