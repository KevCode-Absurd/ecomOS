---
    name: google-shopping
    owner: media-buyer
    version: 1
    invoke_when: the weekly Shopping loop is due, or a first Shopping campaign is needed
    inputs: catalogue, margin, current Shopping structure
    outputs: structure plan, weekly log, change list
    ---
    Purpose: run the Shopping loop the way it earns money: bestsellers first, tiered
    by performance, pruned weekly, never buried inside PMax defaults.

    Steps
    1. On a new account, start Standard Shopping; decline any PMax preselection.
    2. Launch bestsellers only, in one ad group, first.
    3. Pick a structure sized to catalog size and margin spread; tier products by
       rolling performance, each tier its own budget.
    4. Run the weekly loop in order: structure, bidding, negatives, products.
    5. Prune products that spend and click without earning ROAS.
    6. Watch for a competitor discounting a shared product 20-30%; de-prioritise
       that product rather than compete on price blind.
    7. Give a brand-new SKU its own small budget and listing group.

    Checks
    - Bestsellers launched alone before the catalogue widened.
    - The weekly loop covered all four areas, not just bidding.
    - No new SKU diluted the proven bestseller group's data.

    Output: structure plan, weekly optimisation log, change list.

    Example: a competitor cuts price 25% on a shared bestseller -> de-prioritise
    that product in Shopping rather than match the price without a margin plan.
