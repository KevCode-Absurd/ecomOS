---
    name: affiliate-program
    owner: media-buyer
    version: 1
    invoke_when: a new application arrives, the weekly health check is due, or fraud needs a scan
    inputs: applicant profile, affiliate policy, network click/conversion logs
    outputs: approve/reject decisions, onboarding kit, dormant list, fraud flags
    ---
    Purpose: run the affiliate program the way an affiliate manager would, without
    a human touching every routine application, while catching the fraud patterns
    that steal commission without earning it.

    Steps
    1. Screen each application against a fixed rule set: site quality, traffic
       source, category fit, prior brand mentions.
    2. Auto-approve a clear pass, auto-reject clear spam, route only the borderline
       case to the founder.
    3. Generate the approved affiliate's link, coupon code and starter asset kit.
    4. Flag any affiliate with no clicks or sales in 60 days.
    5. Watch for fraud signatures: too-fast click-to-conversion, data-centre or
       proxy ISP traffic, the brand's coupon codes on public aggregator sites
       without rights, or an affiliate bidding on the brand name.
    6. Hold commission on any flagged conversion pending founder review; never
       auto-pay a flagged one.

    Checks
    - Only borderline applications reached the founder.
    - Every held commission has evidence attached, not a hunch.

    Output: approve/reject decisions, onboarding kit, dormant list, leaderboard,
    fraud flag list.

    Example: a conversion completes 40 seconds after the click, from a data-centre
    IP -> flagged, commission held, founder notified before payout.
