---
    name: access-audit
    owner: media-buyer
    version: 1
    invoke_when: the quarterly access review is due
    inputs: account inventory, current access list
    outputs: access audit, change list
    ---
    Purpose: keep account ownership simple and access locked down before it
    becomes an operational risk or a growth blocker.

    Steps
    1. Confirm the ad account, Merchant Center and analytics sit under one master
       login.
    2. Lock down Business Center access before any new team member joins.
    3. Check the $250k/month spend threshold before approving a second ad account
       on the same pixel.
    4. Confirm accounts are not split by country without a currency reason.
    5. List every admin, employee and partner on every connected account.

    Checks
    - No account split exists without a stated currency reason.
    - No second account was opened under the spend threshold.

    Output: access audit, change list.

    Example: spend just crossed $260k/month and checkout in a second currency is
    needed -> a second ad account is now justified; propose it with a reason.
